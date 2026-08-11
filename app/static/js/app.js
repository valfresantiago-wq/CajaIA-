/* =========================================================
   LIBREYA GESTIÓN WEB
   APP.JS
========================================================= */


/* =========================================================
   UTILIDADES GENERALES
========================================================= */

function dinero(valor) {
    return new Intl.NumberFormat(
        "es-AR",
        {
            style: "currency",
            currency: "ARS",
            maximumFractionDigits: 2
        }
    ).format(Number(valor || 0));
}


function numero(valor, decimales = 2) {
    return new Intl.NumberFormat(
        "es-AR",
        {
            minimumFractionDigits: 0,
            maximumFractionDigits: decimales
        }
    ).format(Number(valor || 0));
}


function porcentaje(valor) {
    return `${numero(valor, 2)} %`;
}


/* =========================================================
   ALERTAS / NOTIFICACIONES
========================================================= */

function mostrarNotificacion(
    mensaje,
    tipo = "info",
    duracion = 3500
) {
    const contenedor =
        document.getElementById("notifications");

    if (!contenedor) {
        return;
    }

    const alerta =
        document.createElement("div");

    alerta.className =
        `app-notification notification-${tipo}`;

    alerta.innerHTML = `
        <div class="notification-content">
            <strong>
                ${
                    tipo === "success"
                        ? "Correcto"
                        : tipo === "error"
                        ? "Error"
                        : tipo === "warning"
                        ? "Atención"
                        : "Libreya"
                }
            </strong>

            <span>${mensaje}</span>
        </div>

        <button
            type="button"
            class="notification-close"
            aria-label="Cerrar"
        >
            ×
        </button>
    `;

    contenedor.appendChild(alerta);

    requestAnimationFrame(() => {
        alerta.classList.add(
            "notification-visible"
        );
    });

    const cerrar = () => {
        alerta.classList.remove(
            "notification-visible"
        );

        setTimeout(
            () => alerta.remove(),
            180
        );
    };

    alerta
        .querySelector(".notification-close")
        .addEventListener(
            "click",
            cerrar
        );

    setTimeout(
        cerrar,
        duracion
    );
}


/* =========================================================
   FETCH CENTRALIZADO
========================================================= */

async function apiFetch(
    url,
    opciones = {}
) {
    const config = {
        ...opciones,
        headers: {
            ...(opciones.headers || {})
        }
    };

    if (
        config.body
        &&
        typeof config.body !== "string"
    ) {
        config.headers[
            "Content-Type"
        ] = "application/json";

        config.body =
            JSON.stringify(
                config.body
            );
    }

    try {
        const respuesta =
            await fetch(
                url,
                config
            );

        let datos = null;

        const contentType =
            respuesta.headers.get(
                "content-type"
            );

        if (
            contentType
            &&
            contentType.includes(
                "application/json"
            )
        ) {
            datos =
                await respuesta.json();
        }

        if (!respuesta.ok) {
            const mensaje =
                datos?.detail
                ||
                datos?.message
                ||
                "La operación no pudo completarse.";

            throw new Error(
                mensaje
            );
        }

        return datos;
    }

    catch (error) {
        console.error(
            "Libreya API:",
            error
        );

        throw error;
    }
}


/* =========================================================
   CONFIRMACIÓN SIMPLE
========================================================= */

function confirmarAccion(
    mensaje
) {
    return window.confirm(
        mensaje
    );
}


/* =========================================================
   DEBOUNCE PARA BÚSQUEDAS
========================================================= */

function debounce(
    funcion,
    espera = 280
) {
    let temporizador;

    return function (...args) {
        clearTimeout(
            temporizador
        );

        temporizador =
            setTimeout(
                () =>
                    funcion.apply(
                        this,
                        args
                    ),
                espera
            );
    };
}


/* =========================================================
   ESTADO DE BOTONES
========================================================= */

function setBotonCargando(
    boton,
    cargando,
    texto = "Procesando..."
) {
    if (!boton) {
        return;
    }

    if (cargando) {
        if (
            !boton.dataset
                .textoOriginal
        ) {
            boton.dataset
                .textoOriginal =
                boton.textContent;
        }

        boton.disabled = true;
        boton.classList.add(
            "button-loading"
        );

        boton.textContent =
            texto;
    }

    else {
        boton.disabled = false;
        boton.classList.remove(
            "button-loading"
        );

        if (
            boton.dataset
                .textoOriginal
        ) {
            boton.textContent =
                boton.dataset
                    .textoOriginal;
        }
    }
}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escaparHTML(
    texto
) {
    if (
        texto === null
        ||
        texto === undefined
    ) {
        return "";
    }

    const elemento =
        document.createElement(
            "div"
        );

    elemento.textContent =
        String(texto);

    return elemento.innerHTML;
}


/* =========================================================
   FORMATEO DE FECHAS
========================================================= */

function formatearFecha(
    valor
) {
    if (!valor) {
        return "-";
    }

    const fecha =
        new Date(valor);

    if (
        Number.isNaN(
            fecha.getTime()
        )
    ) {
        return valor;
    }

    return fecha
        .toLocaleDateString(
            "es-AR",
            {
                day: "2-digit",
                month: "2-digit",
                year: "numeric"
            }
        );
}


function formatearFechaHora(
    valor
) {
    if (!valor) {
        return "-";
    }

    const fecha =
        new Date(valor);

    if (
        Number.isNaN(
            fecha.getTime()
        )
    ) {
        return valor;
    }

    return fecha
        .toLocaleString(
            "es-AR",
            {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            }
        );
}


/* =========================================================
   MENÚ MOBILE
========================================================= */

function inicializarSidebar() {
    const sidebar =
        document.getElementById(
            "sidebar"
        );

    const overlay =
        document.getElementById(
            "sidebarOverlay"
        );

    const abrir =
        document.getElementById(
            "sidebarOpen"
        );

    const cerrar =
        document.getElementById(
            "sidebarClose"
        );

    if (!sidebar) {
        return;
    }

    function abrirMenu() {
        sidebar.classList.add(
            "sidebar-open"
        );

        overlay?.classList.add(
            "overlay-visible"
        );
    }

    function cerrarMenu() {
        sidebar.classList.remove(
            "sidebar-open"
        );

        overlay?.classList.remove(
            "overlay-visible"
        );
    }

    abrir?.addEventListener(
        "click",
        abrirMenu
    );

    cerrar?.addEventListener(
        "click",
        cerrarMenu
    );

    overlay?.addEventListener(
        "click",
        cerrarMenu
    );

    window.addEventListener(
        "resize",
        () => {
            if (
                window.innerWidth
                >
                820
            ) {
                cerrarMenu();
            }
        }
    );
}


/* =========================================================
   PÁGINA ACTIVA
========================================================= */

function marcarRutaActiva() {
    const ruta =
        window.location.pathname;

    document
        .querySelectorAll(
            ".nav-item"
        )
        .forEach(
            item => {
                const href =
                    item.getAttribute(
                        "href"
                    );

                if (!href) {
                    return;
                }

                item.classList.remove(
                    "nav-active"
                );

                if (
                    href === "/"
                    &&
                    ruta === "/"
                ) {
                    item.classList.add(
                        "nav-active"
                    );

                    return;
                }

                if (
                    href !== "/"
                    &&
                    ruta.startsWith(
                        href
                    )
                ) {
                    item.classList.add(
                        "nav-active"
                    );
                }
            }
        );
}


/* =========================================================
   FECHA DE TOPBAR
========================================================= */

function actualizarFechaTopbar() {
    const elemento =
        document.getElementById(
            "currentDate"
        );

    if (!elemento) {
        return;
    }

    const ahora =
        new Date();

    const texto =
        ahora.toLocaleDateString(
            "es-AR",
            {
                weekday: "long",
                day: "2-digit",
                month: "long",
                year: "numeric"
            }
        );

    elemento.textContent =
        texto.charAt(0)
            .toUpperCase()
        +
        texto.slice(1);
}


/* =========================================================
   TECLAS RÁPIDAS
========================================================= */

function inicializarAtajos() {
    document.addEventListener(
        "keydown",
        event => {
            if (
                event.key === "Escape"
            ) {
                document
                    .getElementById(
                        "sidebar"
                    )
                    ?.classList.remove(
                        "sidebar-open"
                    );

                document
                    .getElementById(
                        "sidebarOverlay"
                    )
                    ?.classList.remove(
                        "overlay-visible"
                    );
            }
        }
    );
}


/* =========================================================
   INTERACCIÓN VISUAL DE TABLAS
========================================================= */

function inicializarTablas() {
    document
        .querySelectorAll("table")
        .forEach(
            tabla => {
                tabla
                    .querySelectorAll(
                        "tbody tr"
                    )
                    .forEach(
                        fila => {
                            fila.addEventListener(
                                "click",
                                () => {
                                    tabla
                                        .querySelectorAll(
                                            "tbody tr"
                                        )
                                        .forEach(
                                            otra =>
                                                otra.classList
                                                    .remove(
                                                        "row-selected"
                                                    )
                                        );

                                    fila.classList.add(
                                        "row-selected"
                                    );
                                }
                            );
                        }
                    );
            }
        );
}


/* =========================================================
   AUTOCERRAR MENÚ AL NAVEGAR EN MOBILE
========================================================= */

function inicializarLinksSidebar() {
    document
        .querySelectorAll(
            ".sidebar .nav-item"
        )
        .forEach(
            enlace => {
                enlace.addEventListener(
                    "click",
                    () => {
                        if (
                            window.innerWidth
                            <=
                            820
                        ) {
                            document
                                .getElementById(
                                    "sidebar"
                                )
                                ?.classList.remove(
                                    "sidebar-open"
                                );

                            document
                                .getElementById(
                                    "sidebarOverlay"
                                )
                                ?.classList.remove(
                                    "overlay-visible"
                                );
                        }
                    }
                );
            }
        );
}


/* =========================================================
   ARRANQUE GENERAL
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {
        inicializarSidebar();

        marcarRutaActiva();

        actualizarFechaTopbar();

        inicializarAtajos();

        inicializarTablas();

        inicializarLinksSidebar();
    }
);


/* =========================================================
   EXPORTAR FUNCIONES A WINDOW
   PARA USAR DESDE LOS HTML
========================================================= */

window.Libreya = {
    dinero,
    numero,
    porcentaje,
    mostrarNotificacion,
    apiFetch,
    confirmarAccion,
    debounce,
    setBotonCargando,
    escaparHTML,
    formatearFecha,
    formatearFechaHora
};
