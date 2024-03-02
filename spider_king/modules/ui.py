import os
import threading

import wx
from box import Box
from wx.grid import Grid


class SpiderWindow(wx.Frame):
    def __init__(self, config_path, on_task=None, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE):
        self._setting_path = '.settings.yaml'
        self.on_task = on_task
        self._config = Box.from_yaml(filename=config_path, encoding="utf-8")
        if os.path.exists(self._setting_path):
            self._config.settings = Box.from_yaml(filename=self._setting_path, encoding="utf-8")
        else:
            self._config.settings = {}

        wx.Frame.__init__(self, parent, id, self._config.get('name', ''), pos, size, style)

        self.Center()
        self.Init_UI()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def Init_UI(self):
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        params = self._config.get('params', {})
        for param in params:
            self._build_ui(param, self.panel, self.main_sizer, self._config.settings)

        # 添加一个开始任务的按钮
        self.start_button = wx.Button(self.panel, label="开始任务")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.main_sizer.Add(self.start_button, 0, wx.EXPAND | wx.ALL, 15)
        self.panel.SetSizer(self.main_sizer)

    def on_close(self, event):
        Box.to_yaml(self._config.settings, self._setting_path, encoding='utf-8')
        self.Destroy()

    def _build_ui(self, param, parent, sizer, item):
        if param.type == 'group':
            self._build_group(param, parent, sizer, item)
        elif param.type == 'string':
            self._build_string(param, parent, sizer, item)

        elif param.type == 'integer':
            self._build_integer(param, parent, sizer, item)

        elif param.type == 'boolean':
            self._build_boolean(param, parent, sizer, item)

        elif param.type == 'table':
            self._build_table(param, parent, sizer, item)

    def _build_group(self, group, parent, sizer, item):
        if hasattr(item, group.command) is False:
            item[group.command] = {
                'value': {},
                'required': group.get('required', False),
                'type': 'group'
            }
        group_box = wx.StaticBox(parent, label=group.name)
        group_sizer = wx.StaticBoxSizer(group_box, wx.VERTICAL)
        for param in group.params:
            self._build_ui(param, group_box, group_sizer, item[group.command].value)

        sizer.Add(group_sizer, 0, wx.ALL | wx.EXPAND, 5)

    def _build_table(self, table, parent, sizer, item):
        if hasattr(item, table.command) is False:
            item[table.command] = {
                'name': table.name,
                'value': [],
                'required': table.get('required', False),
                'type': 'table'
            }

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 标签和datagrid
        label = wx.StaticText(parent, label=table.name)
        vbox.Add(label, 0, wx.ALIGN_LEFT, 5)
        grid = Grid(parent)
        grid.CreateGrid(0, len(table.params), Grid.SelectRows)
        grid.SetBackgroundColour(wx.Colour(240, 240, 240))
        col_width = (self.GetSize()[0] // len(table.params)) - 30
        for i, param in enumerate(table.params):
            grid.SetColLabelValue(i, param.name)
            grid.SetColSize(i, col_width)

        value = item[table.command].get('value', [])
        for i, row in enumerate(value):
            grid.AppendRows(1)
            for j, param in enumerate(table.params):
                grid.SetCellValue(i, j, row.get(param.command, {}).get('value', None) or param.get('default', ''))

        vbox.Add(grid, 2, wx.EXPAND | wx.TOP, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        add_button = wx.Button(parent, label="添加")
        delete_button = wx.Button(parent, label="删除")
        clear_button = wx.Button(parent, label="清空")
        hbox.Add(add_button, 0, wx.RIGHT, 5)
        hbox.Add(delete_button, 0, wx.RIGHT, 5)
        hbox.Add(clear_button, 0, wx.RIGHT, 5)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT | wx.TOP, 5)
        sizer.Add(vbox, 10, wx.ALL | wx.EXPAND, 10)

        def update_table():
            values = []
            for t in range(grid.GetNumberRows()):
                row = {}
                for j, it in enumerate(table.params):
                    row[it.command] = {
                        'name': it.name,
                        'value': grid.GetCellValue(t, j),
                        'required': it.get('required', False),
                        'type': it.type,
                        'default': it.get('default', None),
                    }

                values.append(row)
            # 排除全部为空的行
            item[table.command].value = values

        def on_add(event):
            grid.AppendRows(1)
            update_table()

        def on_delete(event):
            grid.DeleteRows(grid.GetSelectedRows()[0], 1)
            update_table()

        def on_clear(event):
            grid.ClearGrid()
            grid.DeleteRows(0, grid.GetNumberRows())
            update_table()

        add_button.Bind(wx.EVT_BUTTON, on_add)
        delete_button.Bind(wx.EVT_BUTTON, on_delete)
        clear_button.Bind(wx.EVT_BUTTON, on_clear)

        def OnCellChange(event):
            update_table()

        grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, OnCellChange)

    def _build_string(self, string, parent, sizer, item):
        if hasattr(item, string.command) is False:
            item[string.command] = {
                'name': string.name,
                'value': None,
                'required': string.get('required', False),
                'type': 'string',
                'default': string.get('default', None),
            }

        value = item[string.command].get('value', None) or string.get('default', None)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent, label=f'{string.name}: ')
        hbox.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        text = wx.TextCtrl(parent)
        text.SetValue(value)
        hbox.Add(text, 1, wx.EXPAND)
        sizer.Add(hbox, 0, wx.ALL | wx.EXPAND, 10)

        def on_text(event):
            item[string.command].value = event.GetString()

        text.Bind(wx.EVT_TEXT, on_text)

    def _build_integer(self, integer, parent, sizer, item):
        if hasattr(item, integer.command) is False:
            item[integer.command] = {
                'name': integer.name,
                'value': None,
                'required': integer.get('required', False),
                'type': 'integer',
                'default': integer.get('default', None),
            }
        value = item[integer.command].get('value', None) or integer.get('default', None)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent, label=f'{integer.name}: ')
        hbox.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        text = wx.TextCtrl(parent)
        if value is not None:
            text.SetValue(str(value))
        hbox.Add(text, 1, wx.EXPAND)

        sizer.Add(hbox, 0, wx.ALL | wx.EXPAND, 10)

        def on_text(event):
            s = event.GetString()
            if s.isdigit():
                item[integer.command].value = int(s)
            else:
                item[integer.command].value = None

        text.Bind(wx.EVT_TEXT, on_text)

    def _build_boolean(self, boolean, parent, sizer, item):
        if hasattr(item, boolean.command) is False:
            item[boolean.command] = {
                'name': boolean.name,
                'value': None,
                'required': boolean.get('required', False),
                'type': 'boolean',
                'default': boolean.get('default', False),
            }
        value = item[boolean.command].get('value', None) or boolean.get('default', False)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent, label=f'{boolean.name}: ')
        hbox.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
        text = wx.CheckBox(parent)
        text.SetValue(value)
        hbox.Add(text, 1, wx.EXPAND)

        sizer.Add(hbox, 0, wx.ALL | wx.EXPAND, 10)

        def on_text(event):
            item[boolean.command].value = event.IsChecked()

        text.Bind(wx.EVT_CHECKBOX, on_text)

    def on_start(self, event):
        """
        开始任务
        """
        Box.to_yaml(self._config.settings, self._setting_path, encoding='utf-8')
        try:
            settings = self.get_settings()
        except Exception as e:
            wx.MessageBox(str(e), '错误', wx.OK | wx.ICON_ERROR)
            return

        self.start_button.Enable(False)
        if self.on_task:
            thread = threading.Thread(target=self.on_task, args=[settings, self.on_finish], daemon=True)
            thread.start()

    def on_finish(self):
        def finish():
            self.start_button.Enable(True)

        wx.CallAfter(finish)

    def get_settings(self):
        settings = SettingsParser(self._config.settings)
        return settings.get_settings()


class SettingsParser:
    def __init__(self, settings: Box):
        self._settings = settings

    def get_settings(self, valid=True):
        """
        解析设置项,并验证是否合法
        :return:
        """
        settings = self.get_group_settings(self._settings, valid)
        return settings

    def get_group_settings(self, group: Box, valid=True):
        """
        解析分组设置项
        :param group:
        :param valid:
        :return:
        """
        settings = Box({})
        for setting in group:
            if group[setting].type == 'group':
                settings[setting] = self.get_group_settings(group[setting].value, valid)
            elif group[setting].type == 'string':
                settings[setting] = self.get_string_settings(group[setting], valid)
            elif group[setting].type == 'integer':
                settings[setting] = self.get_integer_settings(group[setting], valid)
            elif group[setting].type == 'boolean':
                settings[setting] = self.get_boolean_settings(group[setting], valid)
            elif group[setting].type == 'table':
                settings[setting] = self.get_table_settings(group[setting], valid)

        return settings

    def get_string_settings(self, string: Box, valid=False):
        """
        解析字符串设置项
        :param string:
        :param valid:
        :return:
        """
        default = string.get('default', None)
        value = string.value
        required = string.get('required', False)
        if required and value is None and valid:
            raise Exception(f'{string.name}是必填项')
        return string.value if string.value else default

    def get_integer_settings(self, integer: Box, valid=False):
        """
        解析整数设置项
        :param integer:
        :param valid:
        :return:
        """
        default = integer.get('default', None)
        value = integer.value
        required = integer.get('required', False)
        if (required and
                (value is None or not value.isdigit())
                and valid):
            raise Exception(f'{integer.name}是必填项,请确认不为空,并且值为整数')
        result = integer.value if integer.value else default
        if isinstance(result, int):
            return result
        elif isinstance(result, str) and result.isdigit():
            return int(result)
        else:
            return None

    def get_boolean_settings(self, boolean: Box, valid=False):
        """
        解析布尔设置项
        :param boolean:
        :param valid:
        :return:
        """
        default = boolean.get('default', None)
        value = boolean.value
        required = boolean.get('required', False)
        if required and value is None and valid:
            raise Exception(f'{boolean.name}是必填项')
        return boolean.value if boolean.value else default

    def get_table_settings(self, table: Box, valid=False):
        """
        解析表格设置项
        :param table:
        :param valid:
        :return:
        """

        def filter_empty_values(d):
            r = []
            for item in d:
                for k, v in item.items():
                    v = v.get('value', None)
                    if v is not None and v != '':
                        r.append(item)
                        break
            return r

        value = table.value
        required = table.get('required', False)
        is_none = value is None or len(value) == 0
        if required and is_none and valid:
            raise Exception(f'{table.name}是必填项')

        tables = filter_empty_values(table.value)
        values = []
        for value in tables:
            result = {}
            for v in value:
                if value[v].type == 'string':
                    result[v] = self.get_string_settings(value[v], valid)
                elif value[v].type == 'integer':
                    result[v] = self.get_integer_settings(value[v], valid)
            values.append(result)
        return values
