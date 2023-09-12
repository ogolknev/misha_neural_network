import flet as ft
import neural_network as nn
from training_sample import training_sample as ts

def main(page: ft.Page):
    
    # VARIABLE DEFENITIONS

    layer = nn.Layer()

    # FUNCTIONS DEFENITIONS

    def nn_save(e, layer=layer):
        layer.save()

    def nn_load(e: ft.FilePickerResultEvent, layer=layer):
        if e.files:
            layer.load(e.files[0].path)


    def grid_decode():
        input = list()
        if grid_dr_h.value and grid_dr_w.value:
            for i in range(len(grid_dr_main_column.controls)):
                for j in range(len(grid_dr_main_column.controls[0].controls)):
                    if grid_dr_main_column.controls[i].controls[j].bgcolor == 'Black':
                        input.append(0)
                    else:
                        input.append(1)
        return input

    def d_learn(e, layer=layer):
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
        grid_dr_txtf_column.controls[3].value = f'{out_num}'
        page.update()
        print(out_num)


    def paint_r(e):
        if e.control.bgcolor == 'Black':
            e.control.bgcolor = 'White'
        else:
            e.control.bgcolor = 'Black'
        page.update()

    def dr_field(e):
        page.update()
        if grid_dr_h.value and grid_dr_w.value:
            print('Ya')
            grid_dr_main_column.clean()
            for i in range(int(grid_dr_h.value)):
                grid_dr_main_column.controls.append(ft.Row(spacing=0))
                for j in range(int(grid_dr_w.value)):
                    grid_dr_main_column.controls[i].controls.append(ft.Container(margin=ft.margin.all(0),
                                                                                 width=30, 
                                                                                 height=30, 
                                                                                 bgcolor='White',
                                                                                 border=ft.border.all(0.5, 'Black'),
                                                                                 on_click=paint_r
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

        grid_dr_txtf_column.controls.append(grid_dr_w)
        grid_dr_txtf_column.controls.append(grid_dr_h)
        grid_dr_txtf_column.controls.append(ft.IconButton(ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=activate))
        grid_dr_txtf_column.controls.append(ft.TextField(label='Answer', width=75, label_style=ft.TextStyle(size=13), on_submit=d_learn))


        grid_dr_txtf_column.controls.append(ft.Row((ft.IconButton(ft.icons.SAVE, on_click=nn_save),
                                                    ft.IconButton(ft.icons.DOWNLOAD, on_click=lambda _: fp_p_load.pick_files(allow_multiple=False))
                                                    )))

        grid_dr_row.controls.append(grid_dr_txtf_column)
        grid_dr_row.controls.append(grid_dr_main_column)

        page.add(
            ft.Text("Работа c обученной нейронной сетью", size=20),
            grid_dr_row,
        )

    def f_p_ts_res_e(e: ft.FilePickerResultEvent, layer = layer):
        layer.__init__(int(nrns_num.value), int(inputs_num.value))
        
        page.clean()
        page.snack_bar = ft.SnackBar(ft.Text(f"Выбрана обучающая выборка: {e.path}"))
        page.snack_bar.open = True
        page.update()
        page.add(
            page_ttl_2,
            ft.Text("Идет обучение, подождите..."),
        )
        nn.learning(layer, ts.ts_init(e.path), 0.01)
        drawer()



    def layer_create(e):
        if not(nrns_num.value and inputs_num.value):
            page.snack_bar = ft.SnackBar(ft.Text("Введите недостающие данные!"))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Нейросеть создана! (1 слой, {nrns_num.value} нейронов c {inputs_num.value} выходами)"))
            page.snack_bar.open = True
            page.clean()
            page.update()
            page.add(page_ttl_2,
                     ft.Row((txt_p_ts,
                             btn_p_ts,
                            )),
                            btn_t_skip
                    )
        page.update()

    # PAGE SETTINGS

    page.title = "misha"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 400

    # CONTROLS DEFENITION

    grid_dr_w = ft.TextField(label='Width', width=75, on_change=dr_field, label_style=ft.TextStyle(size=13))
    grid_dr_h = ft.TextField(label='Height', width=75, on_change=dr_field, label_style=ft.TextStyle(size=13))

    grid_dr_txtf_column = ft.Column()
    grid_dr_row = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START)
    grid_dr_main_column = ft.Column(spacing=0)
    
    page_ttl_2 = ft.Text("Обучение нейронной сети", size=20)
    txt_p_ts = ft.Text("Выберите обучающую выборку", size=15)
    btn_p_ts = ft.TextButton("Обзор...", on_click=lambda _: fp_p_ts.get_directory_path())

    page_ttl_1 = ft.Text("Создание нейронной сети", size=20)
    nrns_num_txt = ft.Text("Количество нейронов в слое", size=15)
    nrns_num = ft.TextField(width=75)
    nrns_num_row = ft.Row((nrns_num, nrns_num_txt, ))
    inputs_num_txt = ft.Text("Количество входов в нейронах", size=15)
    inputs_num = ft.TextField(width=75)
    inputs_num_row = ft.Row((inputs_num, inputs_num_txt))
    btn_l_crte = ft.OutlinedButton("Принять", on_click=layer_create)
    btn_t_skip = ft.OutlinedButton("Продолжить без обучения", on_click=drawer)

    fp_p_ts = ft.FilePicker(on_result=f_p_ts_res_e)
    page.overlay.append(fp_p_ts)

    fp_p_load = ft.FilePicker(on_result=nn_load)
    page.overlay.append(fp_p_load)

    # MAIN BODY

    nrn_crte = ft.Column(
        (
            page_ttl_1,
            nrns_num_row,
            inputs_num_row,
            btn_l_crte
        ),
    )

    page.add(nrn_crte,
             )

    # UPDATE

    page.update()

ft.app(target=main)