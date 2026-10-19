package com.tienda.api.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Objeto de transferencia de datos (DTO) para la creación y actualización de pedidos.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PedidoRequest {

    /**
     * Nombre del cliente que solicita el pedido.
     */
    private String cliente;

    /**
     * Lista de ítems o productos que integran el pedido.
     */
    private List<ItemRequest> items;
}
