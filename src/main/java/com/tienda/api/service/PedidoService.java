package com.tienda.api.service;

import com.tienda.api.dto.ItemRequest;
import com.tienda.api.dto.PedidoRequest;
import com.tienda.api.exception.RecursoNoEncontradoException;
import com.tienda.api.model.DetallePedido;
import com.tienda.api.model.EstadoPedido;
import com.tienda.api.model.Pedido;
import com.tienda.api.model.Producto;
import com.tienda.api.repository.PedidoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class PedidoService {

    private final PedidoRepository pedidoRepository;
    private final ProductoService productoService;

    public List<Pedido> listarTodos() {
        return pedidoRepository.findAll();
    }

    public Pedido buscarPorId(Long id) {
        return pedidoRepository.findById(id)
                .orElseThrow(() -> new RecursoNoEncontradoException("Pedido no encontrado con id " + id));
    }

    @Transactional
    public Pedido crear(PedidoRequest request) {
        if (request.getCliente() == null || request.getCliente().trim().isEmpty()) {
            throw new IllegalArgumentException("El cliente es obligatorio");
        }

        Pedido pedido = Pedido.builder()
                .cliente(request.getCliente().trim())
                .build();

        if (request.getItems() != null) {
            for (ItemRequest itemReq : request.getItems()) {
                pedido.agregarItem(construirItem(itemReq));
            }
        }

        pedido.recalcularTotal();
        log.info("Pedido creado para el cliente {}", pedido.getCliente());
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido actualizar(Long id, PedidoRequest request) {
        Pedido pedido = buscarCarrito(id);

        if (request.getCliente() == null || request.getCliente().trim().isEmpty()) {
            throw new IllegalArgumentException("El cliente es obligatorio");
        }

        pedido.setCliente(request.getCliente().trim());
        pedido.getItems().clear();

        if (request.getItems() != null) {
            for (ItemRequest itemReq : request.getItems()) {
                pedido.agregarItem(construirItem(itemReq));
            }
        }

        pedido.recalcularTotal();
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido agregarItem(Long id, ItemRequest request) {
        Pedido pedido = buscarCarrito(id);
        pedido.agregarItem(construirItem(request));
        pedido.recalcularTotal();
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido quitarItem(Long id, Long itemId) {
        Pedido pedido = buscarCarrito(id);
        boolean eliminado = pedido.getItems().removeIf(item -> item.getId() != null && item.getId().equals(itemId));
        if (!eliminado) {
            throw new RecursoNoEncontradoException("Ítem no encontrado con id " + itemId);
        }
        pedido.recalcularTotal();
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido confirmar(Long id) {
        Pedido pedido = buscarCarrito(id);

        if (pedido.getItems().isEmpty()) {
            throw new IllegalArgumentException("El carrito está vacío");
        }

        for (DetallePedido item : pedido.getItems()) {
            Producto producto = item.getProducto();
            if (producto.getStock() < item.getCantidad()) {
                throw new IllegalArgumentException("Stock insuficiente para " + producto.getNombre());
            }
            producto.setStock(producto.getStock() - item.getCantidad());
        }

        pedido.setEstado(EstadoPedido.CONFIRMADO);
        return pedidoRepository.save(pedido);
    }

    public void eliminar(Long id) {
        pedidoRepository.delete(buscarPorId(id));
    }

    private Pedido buscarCarrito(Long id) {
        Pedido pedido = buscarPorId(id);
        if (pedido.getEstado() != EstadoPedido.CARRITO) {
            throw new IllegalArgumentException("Solo se pueden modificar pedidos en estado CARRITO");
        }
        return pedido;
    }

    private DetallePedido construirItem(ItemRequest request) {
        if (request.getCantidad() == null || request.getCantidad() <= 0) {
            throw new IllegalArgumentException("La cantidad debe ser mayor que cero");
        }
        Producto producto = productoService.buscarPorId(request.getProductoId());
        return DetallePedido.builder()
                .producto(producto)
                .cantidad(request.getCantidad())
                .precioUnitario(producto.getPrecio())
                .subtotal(producto.getPrecio().multiply(BigDecimal.valueOf(request.getCantidad())))
                .build();
    }
}
