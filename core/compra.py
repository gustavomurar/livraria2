from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

class CompraViewSet(ModelViewSet):
    @extend_schema(
        request=None,
        responses={200: None, 400: None},
        description="Finaliza a compra, atualizando o estoque dos livros.",
        summary="Finalizar compra",
    )
    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        compra = self.get_object()

        # Checa se a compra já foi finalizada
        if compra.status != Compra.StatusCompra.CARRINHO:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'status': 'Compra já finalizada'}
            )

        # Garante integridade transacional durante a finalização
        with transaction.atomic():
            for item in compra.itens.all():

                # Valida se o estoque é suficiente para cada livro
                if item.quantidade > item.livro.quantidade:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'Quantidade insuficiente',
                            'livro': item.livro.titulo,
                            'quantidade_disponivel': item.livro.quantidade,
                        }
                    )

                # Atualiza o estoque dos livros
                item.livro.quantidade -= item.quantidade
                item.livro.save()

            # Finaliza a compra: atualiza status
            compra.status = Compra.StatusCompra.FINALIZADO
            compra.save()

        return Response(status=status.HTTP_200_OK, data={'status': 'Compra finalizada'})