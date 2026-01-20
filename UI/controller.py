import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def populate_dd_artists(self):
        artisti = self._model._artists_list
        for a in artisti:
            self._view.ddArtist.options.append(ft.dropdown.Option(key=a.id, text=a.name))
        self._view.update_page()

    def choice_artists(self, e):
        selected_key = e.control.value

        for opt in e.options:
            if opt.key == selected_key:
                self._dd_artists_value = opt.data
            break

    def handle_create_graph(self, e):

        try:
            n_alb = int(self._view.txtNumAlbumMin.value)
        except ValueError:
            self._view.show_alert("Inserire un numero valido")
            return

        self._model.build_graph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato: {self._model.get_num_nodes()} nodi (artisti), "
                    f"{self._model.get_num_edges()} archi")
        )

        self.populate_dd_artists()
        self._view.ddArtist.disabled = False

        self._view.update_page()

    def handle_connected_artists(self, e):
        pass


