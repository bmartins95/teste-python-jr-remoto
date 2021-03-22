from rest_framework import viewsets, status
from rest_framework.views import Response

from api import models, serializers
from api.integrations.github import GithubApi

from django.shortcuts import get_object_or_404

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"

    def retrieve(self, request, login=None):
        """
        Procura a organização na API do Github, se a organização é encontrada a
        função salva os dados da organização no dataset e retorna um dicionário
        com status 200, caso contrário ela retorna um dicionário vazio com status
        404
        """
        api = GithubApi()
        r = api.get_organization(login)

        if r.status_code == status.HTTP_200_OK:
            company = models.Organization(login, name=r.json()["name"], score=api.get_organization_score(login))
            company.save()

            serializer = serializers.OrganizationSerializer(company)
            response = Response(serializer.data, status=r.status_code)
        else:
            response = Response({}, status=r.status_code)

        return response

    def list(self, request, login=None):
        """
        Lista os dados das organizações em ordem decrescente dos scores
        """
        queryset = models.Organization.objects.all().order_by("-score")
        serializer = serializers.OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, login=None):
        """
        Se a organização existe, ela é deletada do dataset e um status
        204 é retornado, caso contrário um status 404 é retornado
        """
        org = get_object_or_404(models.Organization, login=login)
        org.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
