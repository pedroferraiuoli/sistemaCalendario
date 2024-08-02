document.addEventListener('DOMContentLoaded', function() {
    var eventos_serializados = window.eventosSerializados;
    var calendarioEl = document.getElementById('calendario');

    function filtrarEventos() {
        var responsavelFiltro = document.getElementById('filtro-responsavel').value.toLowerCase();
        var tituloFiltro = document.getElementById('filtro-titulo').value.toLowerCase();

        return eventos_serializados.filter(function(evento) {
            var responsavelEvento = evento.responsavel.toLowerCase();
            var tituloEvento = evento.title.toLowerCase();
            return responsavelEvento.includes(responsavelFiltro) && tituloEvento.includes(tituloFiltro);
        });
    }

    function atualizarCalendario(calendar) {
        calendar.removeAllEvents();
        calendar.addEventSource(filtrarEventos());
    }

    function filtrarCardsPorMes(calendar) {
        var dataExibida = calendar.getDate();
        var mesExibido = dataExibida.getMonth();
        var responsavelFiltro = document.getElementById('filtro-responsavel').value.toLowerCase();
        var tituloFiltro = document.getElementById('filtro-titulo').value.toLowerCase();

        document.querySelectorAll('.col-md-6').forEach(function(card) {
            var dataEvento = new Date(card.querySelector('.card').dataset.eventDate + 'T00:00:00');
            var responsavelEvento = card.querySelector('.card-subtitle').textContent.toLowerCase();
            var tituloEvento = card.querySelector('.card-title').textContent.toLowerCase();
            if (dataEvento.getMonth() === mesExibido && responsavelEvento.includes(responsavelFiltro) && tituloEvento.includes(tituloFiltro)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    var calendar = new FullCalendar.Calendar(calendarioEl, {
        initialView: 'dayGridMonth',
        events: eventos_serializados,
        eventDidMount: function(info) {
            if (info.event.extendedProps.obs) {
                info.el.innerHTML += '<div style = "text-align: center;"><i class="bi bi-exclamation-triangle-fill" style = "color: black";></i></div>';
                tippy(info.el, {
                    content: info.event.extendedProps.obs,
                });
            }
        },
        height: 850,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,listMonth,multiMonthYear'
        },
        locale: 'pt-br',
        buttonText: {
            prev: 'Anterior',
            next: 'Próximo',
            today: 'Hoje',
            month: 'Mês',
            list: 'Lista do Mês',
            year: 'Ano'
        },
        datesSet: function() {
            filtrarCardsPorMes(calendar);
        },
        eventClick: function(info) {
            if (info.event.url) {
                window.location.href = info.event.url;
                info.jsEvent.preventDefault();
            }
        },
        moreLinkContent:function(args){
            return '+'+args.num+' Events';
        },
        dayMaxEvents: 8
    });

    calendar.render();

    document.getElementById('filtro-responsavel').addEventListener('input', function() {
        atualizarCalendario(calendar);
        filtrarCardsPorMes(calendar);
    });

    document.getElementById('filtro-titulo').addEventListener('input', function() {
        atualizarCalendario(calendar);
        filtrarCardsPorMes(calendar);
    });

    atualizarCalendario(calendar);
    filtrarCardsPorMes(calendar);
});