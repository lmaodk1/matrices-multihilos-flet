import flet as ft
import threading


# ================= LÓGICA DE HILOS =================
def multiply_row(A, B, result, row, n):
    for j in range(n):
        result[row][j] = sum(A[row][k] * B[k][j] for k in range(n))


# ================= APP =================
def main(page: ft.Page):
    page.title = "Matrices con Hilos"

    # 📱 Tamaño tipo celular
    page.window_width = 360
    page.window_height = 640
    page.window_resizable = False

    page.appbar = ft.AppBar(
        title=ft.Text("Matrices con Hilos"),
        center_title=True,
        bgcolor=ft.Colors.BLUE_600,
        leading=ft.Icon(ft.Icons.CALCULATE),
    )

    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO

    # -------- Selector de modo --------
    mode_selector = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="dynamic", label="NxN dinámico"),
                ft.Radio(value="text", label="Texto manual"),
            ]
        ),
        value="dynamic",
    )

    # ================= MODO DINÁMICO =================
    size_input = ft.TextField(label="Tamaño N", width=120)

    matrix_a_container = ft.Column()
    matrix_b_container = ft.Column()
    matrix_a_fields = []
    matrix_b_fields = []

    def generate_matrices(e):
        nonlocal matrix_a_fields, matrix_b_fields
        matrix_a_container.controls.clear()
        matrix_b_container.controls.clear()
        matrix_a_fields = []
        matrix_b_fields = []

        try:
            n = int(size_input.value)
            if n <= 0 or n > 6:
                result_text.value = "❌ N debe estar entre 1 y 6"
                page.update()
                return

            for i in range(n):
                row_a = []
                row_b = []
                row_ui_a = ft.Row()
                row_ui_b = ft.Row()

                for j in range(n):
                    fa = ft.TextField(width=45)
                    fb = ft.TextField(width=45)
                    row_a.append(fa)
                    row_b.append(fb)
                    row_ui_a.controls.append(fa)
                    row_ui_b.controls.append(fb)

                matrix_a_fields.append(row_a)
                matrix_b_fields.append(row_b)
                matrix_a_container.controls.append(row_ui_a)
                matrix_b_container.controls.append(row_ui_b)

            result_text.value = ""
            page.update()

        except ValueError:
            result_text.value = "❌ Ingrese un número válido"
            page.update()

    # ================= MODO TEXTO =================
    matrix_a_text = ft.TextField(
        label="Matriz A (ej: 1 2; 3 4)",
        multiline=True,
        visible=False,
    )

    matrix_b_text = ft.TextField(
        label="Matriz B (ej: 5 6; 7 8)",
        multiline=True,
        visible=False,
    )

    def parse_matrix(text):
        return [list(map(int, r.split())) for r in text.strip().split(";")]

    # ================= MULTIPLICACIÓN =================
    result_text = ft.Text(size=16)

    def multiply(e):
        try:
            if mode_selector.value == "dynamic":
                n = int(size_input.value)
                A = [[int(matrix_a_fields[i][j].value) for j in range(n)] for i in range(n)]
                B = [[int(matrix_b_fields[i][j].value) for j in range(n)] for i in range(n)]
            else:
                A = parse_matrix(matrix_a_text.value)
                B = parse_matrix(matrix_b_text.value)
                n = len(A)

            if len(A[0]) != len(B):
                result_text.value = "❌ Dimensiones incompatibles"
                page.update()
                return

            result = [[0] * n for _ in range(n)]
            threads = []

            for i in range(n):
                t = threading.Thread(
                    target=multiply_row,
                    args=(A, B, result, i, n)
                )
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            output = "\n".join(" ".join(map(str, row)) for row in result)
            result_text.value = f"Resultado:\n{output}"

        except Exception as ex:
            result_text.value = f"Error: {ex}"

        page.update()

    # ================= CAMBIO DE MODO =================
    def switch_mode(e):
        dynamic = mode_selector.value == "dynamic"

        size_input.visible = dynamic
        matrix_a_container.visible = dynamic
        matrix_b_container.visible = dynamic

        matrix_a_text.visible = not dynamic
        matrix_b_text.visible = not dynamic

        page.update()

    mode_selector.on_change = switch_mode

    # ================= BOTONES =================
    generate_button = ft.ElevatedButton(
        content=ft.Text("Generar matrices"),
        on_click=generate_matrices
    )

    multiply_button = ft.ElevatedButton(
        content=ft.Text("Multiplicar"),
        on_click=multiply
    )

    # ================= UI =================
    page.add(
        ft.Text("🧮 Calculadora de Matrices con Hilos",
                size=18, weight=ft.FontWeight.BOLD),

        mode_selector,

        size_input,
        generate_button,

        ft.Text("Matriz A"),
        matrix_a_container,
        matrix_a_text,

        ft.Text("Matriz B"),
        matrix_b_container,
        matrix_b_text,

        multiply_button,
        result_text
    )


ft.app(target=main)
