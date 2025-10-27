def render_sidebar(menu_items, active_item):
    html = '<div class="sidebar">'
    for item in menu_items:
        cls = "active" if item==active_item else ""
        html += f'<button onclick="showPage(\'{item}\')" class="{cls}">{item}</button>'
    html += "</div>"
    return html
