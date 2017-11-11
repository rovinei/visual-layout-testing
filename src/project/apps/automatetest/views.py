# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.generic.base import View
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.db.models import Q
from django.views.generic import TemplateView
from galenpy.galen_webdriver import GalenRemoteWebDriver
from galenpy.galen_api import (Galen, generate_galen_report)
from galenpy.galen_report import TestReport
from galenpy.exception import (FileNotFoundError, IllegalMethodCallException )
from .utils import generate_random_string
from .models import (Project, TestSession, TestBuild, ScreenshotImage, GalenReport)
from project.apps.screenshot.models import BrowserStackAvailableBrowser
from project.apps.screenshot.forms import ScreenshotAPIForm
import time
import os
import json


def projects_list(request):
    if request.user.is_authenticated():
        context = dict()
        if request.method == 'GET':
            projects = Project.objects.filter(owner__id=request.user.id)
            context.update({
                'page': {
                    'title': 'Automate testing | choose project'
                },
                'projects': projects
            })
            if 'project.uuid' in request.session and 'project.name' in request.session and 'project.owner' in request.session:
                context.update({
                    'current_project': {
                        'uuid': request.session['project.uuid'],
                        'name': request.session['project.name'],
                        'owner': request.session['project.owner'],
                    }
                })
            return render(request, 'automatetest/projects_list.html', context)
        else:
            return HttpResponseNotAllowed(permitted_methods=['GET'])

    else:
        return redirect('/admin/login/?next=/automate/')


def get_project(request, project_uuid):
    if request.user.is_authenticated():
        context = dict()
        if request.method == 'GET':
            try:
                project = Project.objects.get(
                    owner__id=request.user.id,
                    project_uuid=project_uuid
                )
                builds = project.builds.all()
                sessions = project.sessions.all()
                screenshots = project.screenshots.all()
                reports = project.reports.all()

                request.session['project.uuid'] = project.project_uuid
                request.session['project.name'] = project.project_name
                request.session['project.owner'] = project.owner.id
                context.update({
                    'project': project,
                    'screenshots': screenshots,
                    'builds': builds,
                    'sessions': sessions,
                    'reports': reports,
                    'current_project': {
                        'uuid': request.session['project.uuid'],
                        'name': request.session['project.name'],
                        'owner': request.session['project.owner'],
                    }
                })
                return render(request, 'automatetest/project.html', context)
            except ObjectDoesNotExist:
                return redirect('/automate')
        else:
            return HttpResponseNotAllowed()


class CrossBrowserTestAPI(View):

    def get(self, request, project_uuid):
        contexts = dict()
        if request.user.is_authenticated():
            try:
                project = Project.objects.get(
                    owner__id=request.user.id,
                    project_uuid=project_uuid
                )
                request.session['project.uuid'] = project.project_uuid
                request.session['project.name'] = project.project_name
                request.session['project.owner'] = project.owner.id
                contexts.update({
                    'current_project': {
                        'uuid': request.session['project.uuid'],
                        'name': request.session['project.name'],
                        'owner': request.session['project.owner'],
                    }
                })
            except ObjectDoesNotExist:
                contexts.update({
                    'status': 404,
                    'message': 'Oop! the project you are trying to delete does not exists.',
                })
                return redirect('/automate/')

            os_arr = list()
            contexts.update({
                'page_info': {
                    'title': 'Automate Screenshot API | Potential United',
                    'meta': {
                        'keyword': 'Automate testing, cross browser testing, visual regression testing, website layout test'
                    }
                },
                'project': project
            })

            all_browsers = BrowserStackAvailableBrowser.objects.filter(
                Q(os_platform__icontains='os x', os_version__icontains='sierra') |
                Q(os_platform__icontains='windows', os_version='10')
            )
            os_versions = all_browsers.order_by('os_platform', 'os_version').values('os_platform', 'os_version').distinct()
            if os_versions.exists():

                for os_item in os_versions:
                    os_obj = dict()
                    browsers = all_browsers.filter(
                        os_platform=os_item['os_platform'],
                        os_version=os_item['os_version'])
                    browser_versions = browsers.values('browser').distinct()
                    browser_arr = list()
                    for bs in browser_versions:
                        brows = dict()
                        brows_items = browsers.filter(browser=bs['browser'])
                        browser_icon_url = "common/custom/img/icons/svg/"+str(bs['browser']).strip(" ").replace(" ", "-").lower()+".svg"
                        brows.update({
                            'browser_name': bs['browser'],
                            'icon_url': browser_icon_url,
                            'browser_versions': brows_items
                        })
                        browser_arr.append(brows)

                    os_name = os_item['os_platform'] + ' ' + os_item['os_version']
                    icon_url = "common/custom/img/icons/svg/"+str(os_item['os_platform']).strip(" ").replace(" ", "-").lower()+".svg"
                    os_obj.update({
                        'os_name': os_name,
                        'os_platform': os_item['os_platform'],
                        'icon_url': icon_url,
                        'browsers': browser_arr
                    })
                    os_arr.append(os_obj)

                contexts.update({'os_browsers': os_arr})
            else:
                contexts.update({'os_browsers': os_arr})

            screenshot_form = ScreenshotAPIForm(
                initial={
                    'mac_res': '1149x768',
                    'win_res': '1149x768',
                    'screenshot_quality': 'original',
                    'page_url': 'http://ai.pulabo.net/sample06/'
                }
            )

            contexts.update({
                'screenshot_form': screenshot_form
            })
            return render(request, 'automatetest/cross_browser_testing.html', contexts)
        else:
            return redirect('/admin/')

    def post(self, request):
        """
        Accept get method
        """
        contexts = dict()
        if request.user.is_authenticated():
            print(request.POST)
            page_url = request.POST.get('page_url')
            mac_res = request.POST.get('mac_res')
            win_res = request.POST.get('win_res')
            screenshot_quality = request.POST.get('screenshot_quality')
            browsers = request.POST.getlist('browsers')
            build_uuid = request.POST.get('build_uuid', None)
            project_uuid = request.POST.get('project_uuid', None)
            spec_file = request.FILES.get('spec_file', None)
            data = list()
            print(browsers)
            if spec_file is None:
                contexts.update({
                    'status': 400,
                    'message': 'Galen spec file must be present in request.'
                })
                return JsonResponse(contexts)
            print('HEY : 1')
            if project_uuid is not None and project_uuid != '':
                try:
                    project = Project.objects.get(
                        project_uuid=project_uuid,
                        owner__id=request.user.id
                    )
                    print('HEY : 2')
                except ObjectDoesNotExist as e:
                    contexts.update({
                        'status': 404,
                        'message': 'Oop! ' + e.message
                    })
                    return JsonResponse(contexts)
                except:
                    contexts.update({
                        'status': 500,
                        'message': 'Oop! something went wrong, please try again.'
                    })
                    return JsonResponse(contexts)

                if build_uuid is not None and build_uuid != '':
                    print('HEY : 3')
                    try:
                        build = TestBuild.objects.get(
                            build_uuid=build_uuid,
                            project__project_uuid=project_uuid,
                            project__owner__id=request.user.id
                        )
                    except ObjectDoesNotExist as e:
                        contexts.update({
                            'status': 404,
                            'message': 'Oop! ' + e.message
                        })
                        return JsonResponse(contexts)
                    except:
                        contexts.update({
                            'status': 500,
                            'message': 'Oop! something went wrong, please try again.'
                        })
                        return JsonResponse(contexts)
                else:
                    print('HEY : 4')
                    build_count = TestBuild.objects.filter(project=project).count()
                    print('HEY : 4.1 ' + str(build_count+1))
                    try:
                        build = TestBuild(
                            name='Build Version ' + str(build_count+1),
                            project=project
                        )
                        print('Saving build')
                        build.save()
                        print('Build created')
                    except:
                        contexts.update({
                            'status': 500,
                            'message': 'Oop! something went wrong while create build, please try again'
                        })
                        return JsonResponse(contexts)
            else:
                contexts.update({
                    'status': 300,
                    'message': 'Project must be specified in request.'
                })
                return JsonResponse(contexts)

            print('HEY : 4.5')
            for browser in browsers:
                print('HEY : 5 ' + browser)
                origin_browser_name = browser
                os_platform, os_version, browser, device_or_browser_version, is_mobile = str(browser).split('|')
                test_title = origin_browser_name.replace('|', ' ')
                session_report_name = str(origin_browser_name).replace('|', ' ').replace(' ', '-').replace('.', '-').lower()
                print('session Report name :' + session_report_name)
                print('test title :' + test_title)
                browser_data = dict()
                if is_mobile == '1':
                    desired_cap = {
                        'os': str(os_platform).upper(),
                        'os_version': str(os_version),
                        'browser': browser,
                        'device': str(device_or_browser_version),
                        'acceptSslCerts': True,
                        'browserstack.video': False
                    }
                else:
                    desired_cap = {
                        'os': str(os_platform).upper(),
                        'os_version': str(os_version),
                        'browser': browser,
                        'browser_version': str(device_or_browser_version),
                        'acceptSslCerts': True,
                        'browserstack.video': False
                    }
                driver = GalenRemoteWebDriver(remote_url=settings.BS_HUB_URL, desired_capabilities=desired_cap)
                session_uuid = driver.session_id
                driver.get(page_url)
                driver.maximize_window()
                # random_str = generate_random_string(64)
                # img_path = os.path.join(settings.MEDIA_ROOT, "projects/punited/"+random_str+".png")
                # time.sleep(3)

                try:
                    print('HEY : Start galen')
                    check_layout = Galen().check_layout(driver, os.path.join(settings.BASE_DIR, 'project/a.spec'), [], [])
                    print('HEY : Start galen check_layout')
                    TestReport(test_title).add_layout_report_node(test_title, check_layout).finalize()
                    print('HEY : Start galen finalize reports')
                    report_path = '{}/{}/{}'.format(project_uuid, build.build_uuid, session_report_name)
                    full_report_path = os.path.join(
                        settings.GALEN_REPORT_DIR,
                        report_path
                    )
                    print('HEY : Generate report path')
                    generate_galen_report(full_report_path)
                    print('HEY : Start galen generate report')
                    print(build.build_uuid)
                    print(test_title)
                    print(session_uuid)
                    session = TestSession(
                        title=test_title,
                        build=build,
                        project=project,
                        session_uuid=session_uuid
                    )
                    print('Saving session')
                    session.save()
                    print('session saved')

                    print('Create report record')
                    g_report = GalenReport(
                        title=test_title + ' > ' + build.name,
                        report_dir=report_path,
                        project=project,
                        build=build,
                        session=session
                    )
                    print('Saving report record')
                    g_report.save()
                    print('Report record saved')
                    print('HEY : Start serialize report')
                    serialized_report = serializers.serialize(
                        'json',
                        [g_report],
                        fields=('report_uuid', 'title', 'report_dir', 'project', 'build', 'session')
                    )
                    print('HEY : Start serialize session')
                    serialized_session = serializers.serialize(
                        'json',
                        [session,],
                        fields=('title', 'build', 'project', 'session_uuid'))
                    print('HEY : Start serialize session')
                    browser_data.update({
                        'status': 200,
                        'title': test_title,
                        'session': serialized_session,
                        'build': {
                            'uuid': build.build_uuid,
                            'name': build.name
                        },
                        'report': serialized_report,
                        'screenshots': [

                        ]
                    })
                    print('HEY : finished task')

                except:
                    contexts.update({
                        'status': 500,
                        'message': 'Oop! something went wrong, while testing via remote driver.'
                    })
                    browser_data.update({
                        'status': 500,
                        'title': test_title,
                        'message': test_title + ' browser test is failed.'
                    })
                    pass
                finally:
                    print('HEY : Quit Browser')
                    data.append(browser_data)
                    driver.quit()
                    pass

            contexts.update({
                'status': 200,
                'message': 'Automate Cross browser testing finished.',
                'data': data
            })

            return JsonResponse(contexts)

        else:
            contexts.update({
                'status': 403,
                'message': 'Authentication Failed.'
            })
            return JsonResponse(contexts)


class ScreenshotJobAPI(View):
    def get(self, request, project_uuid):
        contexts = dict()
        if request.user.is_authenticated():
            try:
                project = Project.objects.get(owner__id=request.user.id, project_uuid=project_uuid)
                request.session['project.uuid'] = project.project_uuid
                request.session['project.name'] = project.project_name
                request.session['project.owner'] = project.owner.id
                contexts.update({
                    'current_project': {
                        'uuid': request.session['project.uuid'],
                        'name': request.session['project.name'],
                        'owner': request.session['project.owner'],
                    }
                })
            except ObjectDoesNotExist:
                contexts.update({
                    'status': 404,
                    'message': 'Oop! cannot find project you requested.'
                })
                return redirect('/automate/')

            os_arr = list()
            contexts.update({
                'page_info': {
                    'title': 'Automate Screenshot API | Potential United',
                    'meta': {
                        'keyword': 'Automate testing, cross browser testing, visual regression testing, website layout test'
                    }
                },
                'project': project
            })

            all_browsers = BrowserStackAvailableBrowser.objects.filter(
                Q(os_platform__icontains='os x') | Q(os_platform__icontains='windows')
            )
            os_versions = all_browsers.order_by('-os_platform', '-os_version').values('os_platform', 'os_version').distinct()
            if os_versions.exists():

                for os_item in os_versions:
                    os_obj = dict()
                    browsers = all_browsers.filter(
                        os_platform=os_item['os_platform'],
                        os_version=os_item['os_version'])
                    browser_versions = browsers.values('browser').distinct()
                    browser_arr = list()
                    for bs in browser_versions:
                        brows = dict()
                        brows_items = browsers.filter(browser=bs['browser'])
                        browser_icon_url = "common/custom/img/icons/svg/"+str(bs['browser']).strip(" ").replace(" ", "-").lower()+".svg"
                        brows.update({
                            'browser_name': bs['browser'],
                            'icon_url': browser_icon_url,
                            'browser_versions': brows_items
                        })
                        browser_arr.append(brows)

                    os_name = os_item['os_platform'] + ' ' + os_item['os_version']
                    icon_url = "common/custom/img/icons/svg/"+str(os_item['os_platform']).strip(" ").replace(" ", "-").lower()+".svg"
                    os_obj.update({
                        'os_name': os_name,
                        'os_platform': os_item['os_platform'],
                        'icon_url': icon_url,
                        'browsers': browser_arr
                    })
                    os_arr.append(os_obj)

                contexts.update({'os_browsers': os_arr})
            else:
                contexts.update({'os_browsers': os_arr})

            screenshot_form = ScreenshotAPIForm(
                initial={
                    'mac_res': '1149x768',
                    'win_res': '1149x768',
                    'screenshot_quality': 'original',
                    'page_url': 'https://www.p-united.com'
                }
            )

            contexts.update({
                'screenshot_form': screenshot_form
            })
            return render(request, 'automatetest/automate_screenshot.html', contexts)

        else:
            return redirect('/admin/')


class ReportView(View):
    """
    Report detail of testing
    """
    def get(self, request, report_uuid):
        contexts = dict()
        if request.user.is_authenticated():
            try:
                report = GalenReport.objects.get(report_uuid=report_uuid)
                contexts.update({
                    'report': report
                })
            except ObjectDoesNotExist as e:
                contexts.update({
                    'status': 404,
                    'message': e.message
                })
                return redirect('/automate/')

            if 'project.uuid' in request.session and 'project.name' in request.session and 'project.owner' in request.session:
                contexts.update({
                    'current_project': {
                        'uuid': request.session['project.uuid'],
                        'name': request.session['project.name'],
                        'owner': request.session['project.owner'],
                    }
                })

            return render(request, 'automatetest/report_detail.html', contexts)

        else:
            return redirect('/admin/login/?next=/automate/')


class ProjectAjaxView(View):
    """
    Choose or create new testing project
    """
    def get(self, request):
        """
        Get projects belong to user
        :param request:
        :return:
        """
        if request.user.is_authenticated():
            context = dict()
            action = request.GET.get('action', '')
            if action == 'single_project':
                project_uuid = request.GET.get('project_uuid', '')
                if project_uuid != '':
                    try:
                        project = Project.objects.get(project_uuid=project_uuid)
                        serialized_project = serializers.serialize(
                            'json',
                            [project,],
                            fields=('project_uuid', 'project_name', 'description'))
                        context.update({
                            'status': 200,
                            'message': 'Successfully retrieved project.',
                            'project': serialized_project
                        })
                    except ObjectDoesNotExist:
                        context.update({
                            'status': 404,
                            'message': 'Oop! the project you are trying to find does not exists.'
                        })
                        return JsonResponse(context)
                    except:
                        context.update({
                            'status': 500,
                            'message': 'Oop! something went wrong, please try again.'
                        })
                        return JsonResponse(context)

                    return JsonResponse(context)

            elif action == 'user_project':
                user_projects = Project.objects.filter(owner__id =request.user.id)
                projects = serializers.serialize('json', user_projects)
                context.update({
                    'status': 200,
                    'projects': projects
                })

                return JsonResponse(context)
        else:
            JsonResponse({
                'status': 403,
                'message': 'Authentication failed'
            })

    def post(self, request):
        """
        Create new project
        :param request:
        :return: JsonResponse
        """
        if request.user.is_authenticated():
            context = dict()
            action = request.POST.get('action')
            if action == 'create':
                project_name = request.POST.get('project_name', '')
                description = request.POST.get('project_desc', '')
                if project_name != '':
                    try:
                        project = Project(project_name=project_name, description=description)
                        project.owner = request.user
                        project.save()
                        request.session['project_uuid'] = project.project_uuid
                    except ObjectDoesNotExist:
                        context.update({
                            'status': 404,
                            'message': 'Oop! the project you are trying to delete does not exists.',
                        })
                        return JsonResponse(context)
                    except:
                        context.update({
                            'status': 500,
                            'message': 'Oop! something went wrong, please try again.',
                        })
                        return JsonResponse(context)

                context.update({
                    'status': 200,
                    'message': 'Successfully created project ' + project.project_name
                })
                return JsonResponse(context)

            elif action == 'delete':
                project_uuid = request.POST.get('project_uuid', '')
                if project_uuid != '':
                    try:
                        project = Project.objects.get(project_uuid=project_uuid)
                        project.delete()
                        request.session['project_uuid'] = None
                        context.update({
                            'status': 200,
                            'message': 'Successfully deleted project ' + project.project_name
                        })
                    except ObjectDoesNotExist:
                        context.update({
                            'status': 404,
                            'message': 'Oop! the project you are trying to delete does not exists.',
                        })
                        return JsonResponse(context)
                    except:
                        context.update({
                            'status': 500,
                            'message': 'Oop! something went wrong, please try again.',
                        })
                        return JsonResponse(context)

                    return JsonResponse(context)
                else:
                    context.update({
                        'status': 300,
                        'message': 'Project uuid must be specified in request.'
                    })
                    return JsonResponse(context)

            elif action == 'update':
                project_uuid = request.POST.get('project_uuid', '')
                project_name = request.POST.get('project_name', '')
                description = request.POST.get('project_desc', '')
                if project_uuid != '' and project_name != '':
                    try:
                        project = Project.objects.get(project_uuid=project_uuid)
                        project.project_name = project_name
                        project.description = description
                        project.save()
                        serialized_project = serializers.serialize(
                            'json',
                            [project,],
                            fields=('project_uuid', 'project_name', 'description')
                        )
                        context.update({
                            'status': 200,
                            'message': 'Successfully updated project.',
                            'project': serialized_project
                        })
                    except ObjectDoesNotExist:
                        context.update({
                            'status': 404,
                            'message': 'Oop! the project you are trying to update does not exists.',
                        })
                        return JsonResponse(context)
                    except:
                        context.update({
                            'status': 500,
                            'message': 'Oop! something went wrong, please try again.',
                        })
                        return JsonResponse(context)

                    return JsonResponse(context)
                else:
                    context.update({
                        'status': 300,
                        'message': 'Project uuid must be specified in request.'
                    })
                    return JsonResponse(context)

        else:
            JsonResponse({
                'status': 403,
                'message': 'Authentication failed'
            })
