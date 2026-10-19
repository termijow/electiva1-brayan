package com.tienda.api.controller;

import com.tienda.api.dto.ItemRequest;
import com.tienda.api.dto.PedidoRequest;
import com.tienda.api.model.Pedido;
import com.tienda.api.service.PedidoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

 */
@RestController
@RequestMapping("/api/pedidos")
@RequiredArgsConstructor
public class PedidoController {

    private final PedidoService pedidoService;

    @GetMapping
    public ResponseEntity<List<Pedido>> listar() {
        return ResponseEntity.ok(pedidoService.listarTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Pedido> obtener(@PathVariable Long id) {
        return ResponseEntity.ok(pedidoService.buscarPorId(id));
    }

    @PostMapping
    public ResponseEntity<Pedido> crear(@RequestBody PedidoRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(pedidoService.crear(request));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Pedido> actualizar(@PathVariable Long id, @RequestBody PedidoRequest request) {
        return ResponseEntity.ok(pedidoService.actualizar(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        pedidoService.eliminar(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{id}/items")
    public ResponseEntity<Pedido> agregarItem(@PathVariable Long id, @RequestBody ItemRequest request) {
        return ResponseEntity.ok(pedidoService.agregarItem(id, request));
    }

    @DeleteMapping("/{id}/items/{itemId}")
    public ResponseEntity<Pedido> quitarItem(@PathVariable Long id, @PathVariable Long itemId) {
        return ResponseEntity.ok(pedidoService.quitarItem(id, itemId));
    }

    @PatchMapping("/{id}/confirmar")
    public ResponseEntity<Pedido> confirmar(@PathVariable Long id) {
        return ResponseEntity.ok(pedidoService.confirmar(id));
    }
}
