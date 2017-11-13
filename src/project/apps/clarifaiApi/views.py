# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import cStringIO
import json
import time
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.template import loader
from clarifai.rest import ClarifaiApp, Image as ClImage, Concept
from clarifai.rest.client import ApiError, ApiClientError
from django.views.decorators.http import require_http_methods

CL_APP = None
try:
    CL_APP = ClarifaiApp(api_key='ceac8a98d7b148ec82d38b232831aba3')
except ApiError as api_err:
    print(api_err.error_details)


@require_http_methods(['GET'])
def index(request):

    template = loader.get_template('clarifai/index.html')
    context = {
        'page_title': 'PUnited visual web testing | welcome dashboard page'
    }

    return HttpResponse(template.render(context, request), content_type='text/html')


@require_http_methods(['GET', 'POST'])
def add_images_with_concepts(request):

    template = loader.get_template('clarifai/add_images.html')
    context = dict()
    context.update({
        'page_title': 'PUnited visual web testing | Add Images & Concepts'
    })
    print request.POST
    if request.method == 'POST' and request.FILES:
        print request.POST
        print request.FILES
        image_files = request.FILES.getlist('images')
        concepts = request.POST.get('concepts', '')
        not_concepts = request.POST.get('not_concepts', '')
        concepts = [lambda: concepts.split(','), lambda: None][concepts == '']()
        not_concepts = [lambda: not_concepts.split(','), lambda: None][not_concepts == '']()

        if None not in image_files:
            images = []
            for image in image_files:

                # Check whether file need to chunk or not
                if image.multiple_chunks:
                    string_buffer = cStringIO.StringIO()
                    for chunk in image:
                        string_buffer.write(chunk)
                        string_buffer.flush()

                    img_base64 = base64.encodestring(string_buffer.getvalue())
                    string_buffer.close()

                # Small size file should read direct instead
                else:
                    img_string = image.read()
                    img_base64 = base64.encodestring(img_string)

                images.append(ClImage(base64=img_base64, concepts=concepts, not_concepts=not_concepts))

            if len(images) > 0:
                total_images = CL_APP.inputs.bulk_create_images(images)
                status_alert = {
                    'code': 200,
                    'title': 'Done',
                    'message': str(len(total_images))+' images added to clarifai',
                    'type': 'success'
                }
                context.update({'status_alert': status_alert})

            else:
                status_alert = {
                    'code': 300,
                    'title': 'Failed',
                    'message': 'No images object found',
                    'type': 'error'
                }
                context.update({'status_alert': status_alert})

        else:
            status_alert = {
                'code': 400,
                'title': 'Failed',
                'message': 'Concepts and images must be presented in request form',
                'type': 'error'
            }
            context.update({'status_alert': status_alert})

    # Query all concepts
    all_concepts = CL_APP.concepts.get_all()
    all_concepts = [
        {
            'value': concept.concept_id.encode('UTF8'),
            'text': concept.concept_name.encode('UTF8')
        }
        for concept in all_concepts
    ]

    # Query all private models
    all_models = CL_APP.models.get_all(private_only=True)
    all_models = [
        {
            'value': model.model_id.encode('UTF8'),
            'text': model.model_name.encode('UTF8')
        }
        for model in all_models
    ]
    context.update({
        'concepts': all_concepts,
        'models': all_models
    })

    return HttpResponse(template.render(context, request), content_type='text/html')


@require_http_methods(['POST'])
def get_model_concepts(request):
    contexts = dict()
    if request.method == 'POST':
        model_id = request.POST.get('model_id', '')
        if not model_id == '':
            try:
                model_info = CL_APP.models.get(model_id=model_id).get_info(verbose=True)
            except ApiError as api_err:
                model_info = None
                contexts.update({
                    'code': 500,
                    'message': api_err.error_desc
                })
            except ApiClientError as client_err:
                model_info = None
                contexts.update({
                    'code': 500,
                    'message': client_err.error_desc
                })
            finally:
                pass

            if None not in model_info and isinstance(model_info, object):
                if model_info['status']['code'] == 10000:
                    try:
                        model_concepts = model_info['model']['output_info']['data']['concepts']
                    except KeyError as err:
                        contexts.update({
                            'code': 500,
                            'message': str(model_info['model']['name']) + ' model does not contains any concepts yet'
                        })
                        return JsonResponse(contexts)
                    model_concepts = [{'value': concept['id'], 'text': concept['name']} for concept in model_concepts]
                    contexts.update({
                        'code': model_info['status']['code'],
                        'message': model_info['status']['description'],
                        'model_concepts': model_concepts
                    })
                else:
                    contexts.update({
                        'code': model_info['status']['code'],
                        'message': model_info['status']['description']
                    })
        else:
            contexts.update({
                'code': 300,
                'message': 'Model must be specify'
            })

    else:
        contexts.update({
            'code': 405,
            'message': 'Method not allowed'
        })

    return JsonResponse(contexts)


@require_http_methods(['POST'])
def add_concepts_to_model_train(request):
    contexts = dict()
    if request.method == 'POST':
        model_id = request.POST.get('model_id', '')
        concepts = request.POST.get('concepts', '')

        if not model_id == '':
            try:
                model = CL_APP.models.get(model_id)
                concepts = [lambda: concepts.split(','), lambda: []][concepts == '']()
                if len(concepts) > 0:
                    model.add_concepts(concepts)

                model.train(timeout=180)
                contexts.update({
                    'code': 10000,
                    'message': 'Successfully trained '+str(model.model_name.encode('UTF8'))+' model.'
                })
            except ApiError as api_err:
                contexts.update({
                    'code': 500,
                    'message': api_err.error_desc
                })
            except ApiClientError as client_err:
                contexts.update({
                    'code': 500,
                    'message': client_err.error_desc
                })
            finally:
                pass

        else:
            contexts.update({
                'code': 300,
                'message': 'Model must be specify'
            })

    else:
        contexts.update({
            'code': 405,
            'message': 'Method not allowed'
        })

    return JsonResponse(contexts)


@require_http_methods(['POST'])
def create_model_train(request):
    contexts = dict()
    if request.method == 'POST':
        model_id = request.POST.get('model_id', '')
        concepts = request.POST.get('concepts', '')

        if not model_id == '':
            try:
                concepts = [lambda: concepts.split(','), lambda: []][concepts == '']()
                if len(concepts) > 0:
                    model = CL_APP.models.create(model_id=model_id, concepts=concepts)
                    model.train(timeout=180)
                    model_info = {
                        'name': model.model_name,
                        'id': model.model_id
                    }
                    contexts.update({
                        'code': 10000,
                        'message': 'Successfully created & trained ' + str(model.model_name.encode('UTF8')) + ' model.',
                        'model': model_info
                    })
                else:
                    model = CL_APP.models.create(model_id=model_id)
                    model_info = {
                        'name': model.model_name,
                        'id': model.model_id
                    }
                    contexts.update({
                        'code': 10000,
                        'message': 'Successfully created '+str(model.model_name.encode('UTF8'))+' model.',
                        'model': model_info
                    })

            except ApiError as api_err:
                contexts.update({
                    'code': 500,
                    'message': api_err.error_desc
                })
            except ApiClientError as client_err:
                contexts.update({
                    'code': 500,
                    'message': client_err.error_desc
                })
            finally:
                pass

        else:
            contexts.update({
                'code': 300,
                'message': 'Model must be specify'
            })

    else:
        contexts.update({
            'code': 405,
            'message': 'Method not allowed'
        })

    return JsonResponse(contexts)


def prediction_generator(predict_model, predict_images, predict_concepts, min_predict_value):
    select_concept_list = [Concept(concept_id=concept) for concept in predict_concepts]
    try:
        model = CL_APP.models.get(predict_model)
        for image in predict_images:

            # Check whether file need to chunk or not
            if image.multiple_chunks:
                string_buffer = cStringIO.StringIO()
                for chunk in image:
                    string_buffer.write(chunk)
                    string_buffer.flush()

                img_base64 = base64.encodestring(string_buffer.getvalue())
                string_buffer.close()

            # Small size file should read direct instead
            else:
                img_string = image.read()
                img_base64 = base64.encodestring(img_string)

            if len(select_concept_list) > 0:
                predict_result = model.predict_by_base64(img_base64,
                                                         select_concepts=select_concept_list)

            else:
                predict_result = model.predict_by_base64(img_base64, min_value=min_predict_value)

            yield json.dumps(predict_result)

    except ApiError as api_err:
        yield {'code': 500, 'message': api_err.error_details}

    except ApiClientError:
        yield {'code': 500, 'message': 'Error while predict image'}


def gen_test():
    for i in range(1000):
        yield "<p>{}</p><br/>".format('@' * 50 * 1024)

    time.sleep(10)
    for i in range(1000):
        yield "<p>{}</p><br/>".format('T' * 50 * 1024)

def streaming_content(request):
    response = StreamingHttpResponse(gen_test(), content_type='text/html')
    return response


@require_http_methods(['POST'])
def make_prediction(request):
    contexts = dict()

    if request.method == 'POST':

        predict_model = request.POST.get('predict_model', '')
        predict_concepts = request.POST.get('predict_concepts', '')
        predict_concepts = [lambda: predict_concepts.split(','), lambda: []][predict_concepts == '']()
        select_concept_list = [Concept(concept_id=concept) for concept in predict_concepts]
        min_predict_value = request.POST.get('min_predict_value', '0')
        min_predict_value = float(min_predict_value)
        predict_images = request.FILES.getlist('predict_images')

        if not predict_model == '':
            if None not in predict_images:
                return StreamingHttpResponse(gen_test(), content_type='text/plain')
                # return StreamingHttpResponse(prediction_generator(predict_model=predict_model,
                #                                                   predict_images=predict_images,
                #                                                   predict_concepts=predict_concepts,
                #                                                   min_predict_value=min_predict_value),
                #                              content_type='application/json')
                # try:
                #     model = CL_APP.models.get(predict_model)
                #     prediction_data = list()
                #     for image in predict_images:

                #         # Check whether file need to chunk or not
                #         if image.multiple_chunks:
                #             string_buffer = cStringIO.StringIO()
                #             for chunk in image:
                #                 string_buffer.write(chunk)
                #                 string_buffer.flush()

                #             img_base64 = base64.encodestring(string_buffer.getvalue())
                #             string_buffer.close()

                #         # Small size file should read direct instead
                #         else:
                #             img_string = image.read()
                #             img_base64 = base64.encodestring(img_string)

                #         if len(select_concept_list) > 0:
                #             predict_result = model.predict_by_base64(img_base64,
                #                                                      select_concepts=select_concept_list)

                #         else:
                #             predict_result = model.predict_by_base64(img_base64, min_value=min_predict_value)

                #         prediction_data.append(predict_result)

                #     contexts.update({
                #         'code': 10000,
                #         'message': 'Successfully made prediction of '+str(len(predict_images))+' images.',
                #         'prediction_data': prediction_data
                #     })

                # except ApiError as api_err:
                #     contexts.update({
                #         'code': 500,
                #         'message': api_err.error_details
                #     })
                #     pass

                # except ApiClientError:
                #     pass

            else:
                status_alert = {
                    'code': 400,
                    'title': 'Failed',
                    'message': 'Images must be presented in request form',
                    'type': 'error'
                }
                contexts.update({'status_alert': status_alert})

        else:
            contexts.update({
                'code': 300,
                'message': 'Model must be specify'
            })
    else:
        contexts.update({
            'code': 405,
            'message': 'Method not allowed or Request data not valid'
        })

    return JsonResponse(contexts)

