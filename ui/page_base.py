class PageBase:
    """Base class untuk semua halaman"""
    def __init__(self, id_name):
        self.id_name = id_name

    def render_html(self):
        """Kembalikan HTML string halaman"""
        return f"<div id='{self.id_name}'>Dummy page {self.id_name}</div>"
