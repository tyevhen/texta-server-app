from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from texta_api.models.dataset_model import Dataset
from texta_api.models.datarow_model import Datarow

from texta_api.serializers.datarow_serializer import DatarowSerializer
from texta_api.serializers.dataset_serializer import DatasetSerializer

from .helpers.helpers import read_datarows, row_indexes_to_list, is_name_valid

import json

@csrf_exempt
def dataset_controller(request, id=None):
    if request.method == 'GET':
        return get_dataset_or_list(id)

    elif request.method == 'POST':
        return create_dataset(request)

    elif request.method == 'PUT':
        row_to_delete = []
        row_to_delete.append(json.loads(request.body)['datarow'])
        try:
            datarows = row_indexes_to_list(Dataset.objects.get(pk=id).rows)
            if can_delete_rows(datarows, row_to_delete):
                dataset = Dataset.objects.get(pk=id)
                delete_datarows(row_to_delete)
                dataset.rows = [row_id for row_id in datarows if row_id not in row_to_delete]
                dataset.save()
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as exc:
            print('EXCEPTION: ', exc)
            return HttpResponse(status=400)

    elif request.method == 'DELETE':
        return delete_dataset(id)

@csrf_exempt
def dataset_controller_delete_row(request, id=None, row_id=None):
    if request.method == 'DELETE':
        row_to_delete = []
        row_to_delete.append(row_id)
        try:
            datarows = row_indexes_to_list(Dataset.objects.get(pk=id).rows)
            if can_delete_rows(datarows, row_to_delete):
                dataset = Dataset.objects.get(pk=id)
                delete_datarows(row_to_delete)
                dataset.rows = [row_id for row_id in datarows if row_id not in row_to_delete]
                dataset.save()
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as exc:
            print('EXCEPTION: ', exc)
            return HttpResponse(status=400)

@csrf_exempt
def datarows_controller(request, id):
    if request.method == 'POST':
        try:
            dataset = Dataset.objects.get(pk=id)
            dataset.rows = request.POST['datarows']
            dataset.save()
            return HttpResponse(status=200)
        except Dataset.DoesNotExist:
            return HttpResponse(status=400)

@csrf_exempt
def upload_dataset(request, id):
    datarows = read_datarows(request.FILES['file'])
    try:
        datarows_ids = upload_datarows(datarows)
        dataset = Dataset.objects.get(pk=id)
        datarows_list = row_indexes_to_list(dataset.rows)

        if dataset.has_rows():
            new_datarows_list = datarows_list + datarows_ids
            dataset.rows = new_datarows_list
            dataset.save()
        else:
            dataset.rows = datarows_ids
            dataset.save()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=400)

@csrf_exempt
def datarows_view(request):
    return JsonResponse(list(Datarow.objects.all().values()), safe=False)


def get_dataset_or_list(id):
    if id is not None:
        return dataset_view(id)
    else:
        return dataset_list()


def dataset_list():
    return JsonResponse(list(Dataset.objects.all().values()), safe=False)


def dataset_view(id):
    try:
        datarow_ids = Dataset.objects.get(pk=id).rows
        rows = retrieve_datarows(row_indexes_to_list(datarow_ids))
        dataset = {}
        dataset['name'] = Dataset.objects.get(pk=id).name
        dataset['rows'] = rows
        return JsonResponse(
            data={
                'id': id,
                'name': Dataset.objects.get(pk=id).name,
                'rows': rows
            }
        )
    except Dataset.DoesNotExist:
        return HttpResponse(status=400)

def delete_dataset(id):
    try:
        dataset = Dataset.objects.get(pk=id)
        rows = row_indexes_to_list(dataset.rows)
        response = dataset.delete()
        resp = delete_datarows(rows)
        return resp, response
    except Dataset.DoesNotExist:
        return HttpResponse(status=400)


def create_dataset(request):
    try:
        new_dataset_name = json.loads(request.body, encoding='utf8')['dataset_name']
        if is_name_valid(new_dataset_name):
            dataset_serializer = DatasetSerializer(data={'name': new_dataset_name})
            if dataset_serializer.is_valid(raise_exception=True):
                try:
                    new_dataset = dataset_serializer.save()
                    return HttpResponse(new_dataset.pk, status=201)
                except:
                    return HttpResponse(status=400)
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)
    except Exception as exc:
        print('Name dataset exception: ', exc)
        return HttpResponse(status=400)

def upload_datarows(datarows):
    datarows_ids = []
    try:
        for datarow in datarows:
            datarow_serializer = DatarowSerializer(data={'content': json.dumps(json.loads(datarow, encoding='utf8'))})
            if datarow_serializer.is_valid(raise_exception=True):
                saved_datarow = datarow_serializer.save()
                datarows_ids.append(saved_datarow.id)
    except Exception as exc:
        print('Exception: ', exc)
        return HttpResponse(status=400)
    return datarows_ids


def delete_datarows(datarows_ids):
    for id in datarows_ids:
        try:
            datarow = Datarow.objects.get(pk=id)
            datarow.delete()
            return HttpResponse(status=200)
        except Dataset.DoesNotExist:
            return HttpResponse(status=400)


def retrieve_datarows(datarow_ids):
    datarows = []
    try:
        for id in datarow_ids:
            datarow = json.loads(Datarow.objects.get(pk=id).content, encoding='utf8')
            row_data = {}
            row_data['id'] = id
            row_data['content'] = datarow
            datarows.append(row_data)
    except Exception as exc:
        print('Exception: ', exc)
    return datarows


def can_delete_rows(old_datarow_ids, new_datarow_ids):
    flags = [id in old_datarow_ids for id in new_datarow_ids]
    return all(flags)
