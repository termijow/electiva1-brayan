package com.tienda.api.service;

import com.tienda.api.dto.ItemRequest;
import com.tienda.api.dto.PedidoRequest;
import com.tienda.api.exception.RecursoNoEncontradoException;
import com.tienda.api.model.DetallePedido;
import com.tienda.api.model.EstadoPedido;
import com.tienda.api.model.Pedido;
import com.tienda.api.model.Producto;
import com.tienda.api.repository.PedidoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class PedidoServiceTest {

    @Mock
    private PedidoRepository pedidoRepository;

    @Mock
    private ProductoService productoService;

    @InjectMocks
    private PedidoService pedidoService;

    private Producto producto;

    @BeforeEach
    void setUp() {
        producto = Producto.builder()
                .id(1L)
                .nombre("Mouse Inalámbrico")
                .precio(new BigDecimal("50000.00"))
                .stock(10)
                .build();
    }

    @Test
    void crear_conItems_calculaSubtotalesYTotalCorrectamente() {
        when(productoService.buscarPorId(1L)).thenReturn(producto);
        when(pedidoRepository.save(any(Pedido.class))).thenAnswer(inv -> inv.getArgument(0));

        ItemRequest itemReq = new ItemRequest(1L, 2);
        PedidoRequest request = new PedidoRequest("Juan Pérez", List.of(itemReq));

        Pedido resultado = pedidoService.crear(request);

        assertNotNull(resultado);
        assertEquals("Juan Pérez", resultado.getCliente());
        assertEquals(EstadoPedido.CARRITO, resultado.getEstado());
        assertEquals(1, resultado.getItems().size());
        assertEquals(new BigDecimal("100000.00"), resultado.getTotal());
        assertEquals(new BigDecimal("100000.00"), resultado.getItems().get(0).getSubtotal());
    }

    @Test
    void crear_sinCliente_lanzaIllegalArgumentException() {
        PedidoRequest request = new PedidoRequest("", List.of());

        assertThrows(IllegalArgumentException.class, () -> pedidoService.crear(request));
    }

    @Test
    void confirmar_conStockSuficiente_cambiaAConfirmadoYDescuentaStock() {
        DetallePedido detalle = DetallePedido.builder()
                .id(10L)
                .producto(producto)
                .cantidad(3)
                .precioUnitario(producto.getPrecio())
                .subtotal(new BigDecimal("150000.00"))
                .build();

        Pedido pedido = Pedido.builder()
                .id(1L)
                .cliente("Brayan")
                .estado(EstadoPedido.CARRITO)
                .items(new ArrayList<>(List.of(detalle)))
                .total(new BigDecimal("150000.00"))
                .build();
        detalle.setPedido(pedido);

        when(pedidoRepository.findById(1L)).thenReturn(Optional.of(pedido));
        when(pedidoRepository.save(any(Pedido.class))).thenAnswer(inv -> inv.getArgument(0));

        Pedido confirmado = pedidoService.confirmar(1L);

        assertEquals(EstadoPedido.CONFIRMADO, confirmado.getEstado());
        assertEquals(7, producto.getStock()); // 10 - 3 = 7
    }

    @Test
    void confirmar_conStockInsuficiente_lanzaIllegalArgumentException() {
        DetallePedido detalle = DetallePedido.builder()
                .id(10L)
                .producto(producto)
                .cantidad(15) // stock es 10
                .precioUnitario(producto.getPrecio())
                .subtotal(new BigDecimal("750000.00"))
                .build();

        Pedido pedido = Pedido.builder()
                .id(1L)
                .cliente("Brayan")
                .estado(EstadoPedido.CARRITO)
                .items(new ArrayList<>(List.of(detalle)))
                .total(new BigDecimal("750000.00"))
                .build();
        detalle.setPedido(pedido);

        when(pedidoRepository.findById(1L)).thenReturn(Optional.of(pedido));

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> pedidoService.confirmar(1L));
        assertTrue(ex.getMessage().contains("Stock insuficiente"));
    }

    @Test
    void quitarItem_recalculaTotal() {
        DetallePedido detalle1 = DetallePedido.builder()
                .id(101L)
                .producto(producto)
                .cantidad(1)
                .subtotal(new BigDecimal("50000.00"))
                .build();

        DetallePedido detalle2 = DetallePedido.builder()
                .id(102L)
                .producto(producto)
                .cantidad(2)
                .subtotal(new BigDecimal("100000.00"))
                .build();

        Pedido pedido = Pedido.builder()
                .id(1L)
                .cliente("Brayan")
                .estado(EstadoPedido.CARRITO)
                .items(new ArrayList<>(List.of(detalle1, detalle2)))
                .total(new BigDecimal("150000.00"))
                .build();

        when(pedidoRepository.findById(1L)).thenReturn(Optional.of(pedido));
        when(pedidoRepository.save(any(Pedido.class))).thenAnswer(inv -> inv.getArgument(0));

        Pedido actualizado = pedidoService.quitarItem(1L, 101L);

        assertEquals(1, actualizado.getItems().size());
        assertEquals(new BigDecimal("100000.00"), actualizado.getTotal());
    }
}
