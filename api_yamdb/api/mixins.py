from rest_framework import viewsets, mixins


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Класс представления DRF, содержащий методы для получения списка объектов,
    создания новых объектов и удаления уже существующих.
    """
