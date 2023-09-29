import flet as ft
import neural_network as nn
from training_sample import training_sample as ts
from pynput import mouse

mclick = None

def main(page: ft.Page):
    
    # VARIABLE DEFENITIONS

    layer = nn.Layer()

    # FUNCTIONS DEFENITIONS

    def on_click(x, y, button, pressed):
        global mclick
        if pressed:
            if button == mouse.Button.left:
                mclick = 'left'
            elif button == mouse.Button.right:
                mclick = 'right'
        else:
            mclick = None
        print(mclick)


    listener = mouse.Listener(on_click=on_click)
    listener.start()

    def nn_grid_viewer(e):
        page.update()
        if grid_draw_h.value and grid_draw_w.value:
            grid_draw_draw_column.clean()
            max_weight = max(layer.neurons[int(answer_txtfield.value)].weight)
            min_weight = min(layer.neurons[int(answer_txtfield.value)].weight)
            neuron_num = int(answer_txtfield.value)
            print(neuron_num)
            step = ((max_weight - min_weight) / 255)
            for i in range(int(grid_draw_h.value)):
                grid_draw_draw_column.controls.append(ft.Row(spacing=0))
                for j in range(int(grid_draw_w.value)):
                    
                    weight_num = int(grid_draw_w.value) * i + j
                    print(weight_num)
                    color = f'#{"%x" % int(-(min_weight - layer.neurons[neuron_num].weight[weight_num]) / step)}' + '000000'
                    print(color)
                    grid_draw_draw_column.controls[i].controls.append(ft.Container(margin=ft.margin.all(0),
                                                                                 width=250 / max(int(grid_draw_w.value), int(grid_draw_h.value)), 
                                                                                 height=250 / max(int(grid_draw_w.value), int(grid_draw_h.value)),
                                                                                 bgcolor=color,
                                                                                 ))
        page.update()


    def nn_save(e, layer=layer):
        layer.save()

    def nn_load(e: ft.FilePickerResultEvent, layer=layer):
        if e.files:
            layer.load(e.files[0].path)


    def grid_decode():
        input = list()
        if grid_draw_h.value and grid_draw_w.value:
            for i in range(len(grid_draw_draw_column.controls)):
                for j in range(len(grid_draw_draw_column.controls[0].controls)):
                    if grid_draw_draw_column.controls[i].controls[j].bgcolor == 'Black':
                        input.append(0)
                    else:
                        input.append(1)
        return input

    def add_learning(e, layer=layer):
        print(nn.out_encode(int(e.control.value), layer.neurons_num))
        input = list()
        input.append(grid_decode())
        output_ = list()
        output_.append(nn.out_encode(int(e.control.value), layer.neurons_num))
        if nn.learning(layer, (input, output_), 0.01) > 0:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ответ учтен"))
            page.snack_bar.open = True
            page.update()

    def activate(e, layer=layer):
        input = grid_decode()
        out = layer.activate(input)
        out_num = 0
        out_num = nn.out_decode(out)
        grid_draw_control_column.controls[3].value = f'{out_num}'
        page.update()
        print(out_num)


    def paint_grid(e):
        if mclick:
            if mclick == 'left':
                e.control.bgcolor = 'Black'
            elif mclick == 'right':
                e.control.bgcolor = 'White'
            grid_draw_draw_column.controls[e.control.data].update()


    def draw_canvas(e):
        page.update()
        if grid_draw_h.value and grid_draw_w.value:
            grid_draw_draw_column.clean()
            for i in range(int(grid_draw_h.value)):
                grid_draw_draw_column.controls.append(ft.Row(spacing=0))
                for _ in range(int(grid_draw_w.value)):
                    grid_draw_draw_column.controls[i].controls.append(ft.Container(margin=ft.margin.all(0),
                                                                                 width=250 / max(int(grid_draw_w.value), int(grid_draw_h.value)), 
                                                                                 height=250 / max(int(grid_draw_w.value), int(grid_draw_h.value)), 
                                                                                 bgcolor='White',
                                                                                 border=ft.border.all(0.05, 'Black'),
                                                                                 on_hover=paint_grid,
                                                                                 on_click=paint_grid,
                                                                                 data=i
                                                                                 ))
        page.update()


    def drawer(e = None, layer = layer):
        page.clean()
        if not e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Нейросеть обучена"))
            page.snack_bar.open = True
        else:
            layer.__init__(int(nrns_num.value), int(inputs_num.value))
        page.update()

        grid_draw_control_column.controls.append(grid_draw_w)
        grid_draw_control_column.controls.append(grid_draw_h)
        grid_draw_control_column.controls.append(ft.Row((ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=activate),
                                                         ft.IconButton(ft.icons.REMOVE_RED_EYE_OUTLINED, on_click=nn_grid_viewer))
                                                        ))
        grid_draw_control_column.controls.append(answer_txtfield)


        grid_draw_control_column.controls.append(ft.Row((ft.IconButton(ft.icons.SAVE, on_click=nn_save),
                                                    ft.IconButton(ft.icons.DOWNLOAD, on_click=lambda _: filep_load.pick_files(allow_multiple=False))
                                                    )))

        grid_draw_row.controls.append(grid_draw_control_column)
        grid_draw_row.controls.append(grid_draw_draw_column)

        page.add(
            ft.Text("Работа c обученной нейронной сетью", size=20),
            grid_draw_row,
        )

    def ts_filep_event(e: ft.FilePickerResultEvent, layer = layer):
        layer.__init__(int(nrns_num.value), int(inputs_num.value))
        
        page.clean()
        page.snack_bar = ft.SnackBar(ft.Text(f"Выбрана обучающая выборка: {e.path}"))
        page.snack_bar.open = True
        page.update()
        page.add(
            page_title_2,
            ft.Text("Идет обучение, подождите..."),
        )
        nn.learning(layer, ts.ts_init(e.path), 0.01)
        drawer()



    def nn_creation(e):
        if not(nrns_num.value and inputs_num.value):
            page.snack_bar = ft.SnackBar(ft.Text("Введите недостающие данные!"))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Нейросеть создана! (1 слой, {nrns_num.value} нейронов c {inputs_num.value} выходами)"))
            page.snack_bar.open = True
            page.clean()
            page.update()
            page.add(page_title_2,
                     ft.Row((txt_filep_ts,
                             btn_filep_ts,
                            )),
                            btn_training_skip
                    )
        page.update()

    # PAGE SETTINGS

    page.title = "misha"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 400
    page.theme_mode = ft.ThemeMode("light")

    # CONTROLS DEFENITION

    grid_draw_w = ft.TextField(label='Width', width=75, on_change=draw_canvas, label_style=ft.TextStyle(size=13))
    grid_draw_h = ft.TextField(label='Height', width=75, on_change=draw_canvas, label_style=ft.TextStyle(size=13))

    grid_draw_control_column = ft.Column()
    grid_draw_row = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START)
    grid_draw_draw_column = ft.Column(spacing=0)
    
    page_title_2 = ft.Text("Обучение нейронной сети", size=20)
    txt_filep_ts = ft.Text("Выберите обучающую выборку", size=15)
    btn_filep_ts = ft.TextButton("Обзор...", on_click=lambda _: filep_ts.get_directory_path())

    page_title_1 = ft.Text("Создание нейронной сети", size=20)
    nrns_num_txt = ft.Text("Количество нейронов в слое", size=15)
    nrns_num = ft.TextField(width=75)
    nrns_num_row = ft.Row((nrns_num, nrns_num_txt, ))
    inputs_num_txt = ft.Text("Количество входов в нейронах", size=15)
    inputs_num = ft.TextField(width=75)
    inputs_num_row = ft.Row((inputs_num, inputs_num_txt))
    btn_layer_crte = ft.OutlinedButton("Принять", on_click=nn_creation)
    btn_training_skip = ft.OutlinedButton("Продолжить без обучения", on_click=drawer)
    answer_txtfield = ft.TextField(label='Answer', width=75, label_style=ft.TextStyle(size=13), on_submit=add_learning)

    filep_ts = ft.FilePicker(on_result=ts_filep_event)
    page.overlay.append(filep_ts)

    filep_load = ft.FilePicker(on_result=nn_load)
    page.overlay.append(filep_load)

    # MAIN BODY

    nrn_crte = ft.Column(
        (
            page_title_1,
            nrns_num_row,
            inputs_num_row,
            btn_layer_crte
        ),
    )

    page.add(nrn_crte,
             )

    # UPDATE

    page.update()

ft.app(target=main)