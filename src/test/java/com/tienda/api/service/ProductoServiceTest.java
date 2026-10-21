package com.tienda.api.service;

import com.tienda.api.exception.RecursoNoEncontradoException;
import com.tienda.api.model.Producto;
import com.tienda.api.repository.ProductoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ProductoServiceTest {

    @Mock
    private ProductoRepository productoRepository;

    @InjectMocks
    private ProductoService productoService;

    private Producto producto;

    @BeforeEach
    void setUp() {
        producto = Producto.builder()
                .id(1L)
                .nombre("Laptop Gamer")
                .descripcion("Laptop 16GB RAM, RTX 4060")
                .precio(new BigDecimal("3500000.00"))
                .stock(10)
                .build();
    }

    @Test
    void listarTodos_retornaListaDeProductos() {
        when(productoRepository.findAll()).thenReturn(List.of(producto));

        List<Producto> resultado = productoService.listarTodos();

        assertNotNull(resultado);
        assertEquals(1, resultado.size());
        assertEquals("Laptop Gamer", resultado.get(0).getNombre());
        verify(productoRepository, times(1)).findAll();
    }

    @Test
    void buscarPorId_existente_retornaProducto() {
        when(productoRepository.findById(1L)).thenReturn(Optional.of(producto));

        Producto resultado = productoService.buscarPorId(1L);

        assertNotNull(resultado);
        assertEquals(1L, resultado.getId());
        assertEquals("Laptop Gamer", resultado.getNombre());
    }

    @Test
    void buscarPorId_noExistente_lanzaRecursoNoEncontradoException() {
        when(productoRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(RecursoNoEncontradoException.class, () -> productoService.buscarPorId(99L));
    }

    @Test
    void crear_guardaYRetornaProducto() {
        when(productoRepository.save(any(Producto.class))).thenReturn(producto);

        Producto resultado = productoService.crear(producto);

        assertNotNull(resultado);
        assertEquals("Laptop Gamer", resultado.getNombre());
        verify(productoRepository, times(1)).save(producto);
    }

    @Test
    void actualizar_productoExistente_modificaCampos() {
        when(productoRepository.findById(1L)).thenReturn(Optional.of(producto));
        when(productoRepository.save(any(Producto.class))).thenAnswer(inv -> inv.getArgument(0));

        Producto actualizacion = Producto.builder()
                .nombre("Laptop Pro")
                .descripcion("Actualizada")
                .precio(new BigDecimal("4000000.00"))
                .stock(5)
                .build();

        Producto resultado = productoService.actualizar(1L, actualizacion);

        assertEquals("Laptop Pro", resultado.getNombre());
        assertEquals("Actualizada", resultado.getDescripcion());
        assertEquals(new BigDecimal("4000000.00"), resultado.getPrecio());
        assertEquals(5, resultado.getStock());
    }

    @Test
    void eliminar_productoExistente_llamaDelete() {
        when(productoRepository.findById(1L)).thenReturn(Optional.of(producto));
        doNothing().when(productoRepository).delete(producto);

        productoService.eliminar(1L);

        verify(productoRepository, times(1)).delete(producto);
    }
}
