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
        config
