from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()

for i in range(0, 500):
    factory.get('dataset/${}'.format(i))

factory.post('dataset/', {'dataset_name': ''})