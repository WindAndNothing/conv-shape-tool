import tkinter as tk
from tkinter import ttk

#('Linear', 'channel', 'Conv2d', 'Normalization', 'Dropout')
net_type = ('Conv2d')


class LayerOption:
    def __init__(self, frame, layer_type):
        self.frame = frame
        self.type = layer_type
        self.name_list = []
        self.defult_value = []
        self.value_dict = {}
        if self.type == 'Linear':
            self.name_list = ['input', 'output']
        elif self.type == 'channel':
            self.name_list = ['number']
        elif self.type == 'Conv2d':
            self.name_list = ['channel_out', 'kernal_size', 'stride', 'padding']
            self.defult_value = [1, 3, 1, 0]
            pass
        elif self.type == net_type[2]:
            pass
        elif self.type == net_type[3]:
            pass
        self.setbox(self.name_list, self.defult_value)

    def setbox(self, namelist, valuelist):
        for i, (n, v) in enumerate(zip(namelist, valuelist)):
            tk.Label(self.frame, text=n).grid(column=i, row=0)
            self.value_dict[n] = tk.IntVar(value=v)
            tk.Entry(self.frame, width=4, textvariable=self.value_dict[n]).grid(column=i, row=1)

    def forward(self, x):
        if self.type == 'Linear':
            pass
        elif self.type == 'channel':
            pass
        elif self.type == 'Conv2d':
            return self.conv(x[0]), self.conv(x[1]), self.value_dict['channel_out'].get()
            pass
        elif self.type == net_type[2]:
            pass
        elif self.type == net_type[3]:
            pass
        return None

    def conv(self, h):
        h = (h + 2 * self.value_dict['padding'].get() - self.value_dict['kernal_size'].get()) / self.value_dict['stride'].get() + 1
        return int(h)


class Block:
    def __init__(self, root, name=None):
        if name is None:
            self.name = 'block'
        else:
            self.name = name
        self.root = root
        self.type = None
        self.option = None
        self.frame = tk.LabelFrame(self.root, text=self.name)
        self.frame.pack()
        self.type_menu = ttk.Combobox(self.frame, width=15)
        self.type_menu['value'] = net_type
        self.type_menu.bind("<<ComboboxSelected>>", self.select_net)
        self.type_menu.grid(column=0, row=0)
        self.delete_button = tk.Button(self.frame, text='X', command=self.delete,
                                       width=3, height=1, padx=0, pady=0, borderwidth=1,
                                       bg='#FF2424')
        self.delete_button.grid(column=2, row=0)
        self.option_grid = tk.Frame(self.frame)
        self.option_grid.grid(column=0, columnspan=3, row=1)
        self.option_frame = tk.Frame(self.option_grid)
        self.option_frame.pack()
        self.delete_method = None

    def delete(self):
        self.frame.destroy()
        self.delete_method(self)
        del self

    def select_net(self, event):
        type = self.type_menu.get()
        # 如果选择没改变不做操作
        if type == self.type:
            return None
        # 选择发生改变清除操作框 并建立新操作框
        self.option_frame.destroy()
        self.type = type
        self.option_frame = tk.Frame(self.option_grid)
        self.option_frame.pack()
        self.option = LayerOption(self.option_frame, self.type)

    def forward(self, x):
        return self.option.forward(x)

    def __str__(self):
        return f'{self.name}:{self.type}'


class Manage:
    def __init__(self, root):
        self.root = root
        self.input_block = InputBlock(self, self.root)
        self.end_block = ConfigBlock(self, self.root)
        self._forward_chain = {self.input_block: [self.end_block]}
        self._reverse_chain = {self.end_block: [self.input_block]}

    def _add_connect(self, block, root_block):
        if type(block) is not list and type(root_block) is not list:
            self._forward_chain[root_block].append(block)
            self._reverse_chain[block].append(root_block)
        elif type(block) is list and type(root_block) is not list:
            for b in block:
                self._add_connect(b, root_block)
        elif type(block) is not list and type(root_block) is list:
            for b in root_block:
                self._add_connect(block, b)
        else:
            raise ValueError('block and root_block should not are list at the same time')

    def _delete_connect(self, block, root_block):
        if type(block) is not list and type(root_block) is not list:
            self._forward_chain[root_block].remove(block)
            self._reverse_chain[block].remove(root_block)
        elif type(block) is list and type(root_block) is not list:
            for b in block:
                self._delete_connect(b, root_block)
        elif type(block) is not list and type(root_block) is list:
            for b in root_block:
                self._delete_connect(block, b)
        else:
            raise ValueError('block and root_block should not are list at the same time')

    def add_block(self, block: Block):
        block.delete_method = self.delete_block
        self._reverse_chain[block] = []
        self._forward_chain[block] = []
        self._add_connect(block, self._reverse_chain[self.end_block])
        self._add_connect(self.end_block, block)
        self._delete_connect(self.end_block, self._reverse_chain[self.end_block])

    def delete_block(self, block):
        root_block = self._reverse_chain[block]
        next_block = self._forward_chain[block]
        if len(root_block) == 1:
            for b in next_block:
                self._add_connect(b, root_block[0])
        elif len(next_block) == 1:
            for b in root_block:
                self._add_connect(next_block[0], b)
        for b in root_block:
            self._delete_connect(block, b)
        for b in next_block:
            self._delete_connect(b, block)
        self._forward_chain.pop(block)
        self._reverse_chain.pop(block)

    def forward(self):
        shape_dict = {self.input_block: self.input_block.get}
        nodes = [self.end_block]
        while nodes:
            node = nodes[-1]
            can_calculate = True
            if node in shape_dict:
                nodes.remove(node)
            for sub_node in self._reverse_chain[node]:
                if sub_node in shape_dict:
                    pass
                else:
                    can_calculate = False
                    nodes.append(sub_node)
            if can_calculate:
                cal_list = self._reverse_chain[node].copy()
                shape = list(shape_dict[cal_list.pop(0)])
                for sub_node in cal_list:
                    sub_shape = shape_dict[sub_node]
                    if shape[:2] == sub_shape[:2]:
                        shape[2] += sub_shape[2]
                shape_dict[node] = node.forward(shape)
                nodes.pop(-1)
        #print(shape_dict)
        self.end_block.display_shape(shape_dict[self.end_block])

    def __test_chain(self):
        for b, l in self._forward_chain.items():
            for sb in l:
                if b not in self._reverse_chain[sb]:
                    print(self._forward_chain)
                    print(self._reverse_chain)
                    break
        for b, l in self._reverse_chain.items():
            for sb in l:
                if b not in self._forward_chain[sb]:
                    print(self._forward_chain)
                    print(self._reverse_chain)
                    break


class InputBlock:
    def __init__(self, manager, root):
        self.manager = manager
        self.root = root
        self.size_frame = tk.Frame(self.root)
        self.size_frame.pack()
        tk.Label(self.size_frame, text='x:').grid(column=0, row=0)
        tk.Label(self.size_frame, text='y:').grid(column=1, row=0)
        tk.Label(self.size_frame, text='channels:').grid(column=2, row=0)

        self.input_shape = (tk.IntVar(), tk.IntVar(), tk.IntVar())
        self.input_x = tk.Entry(self.size_frame, width=10, textvariable=self.input_shape[0])
        self.input_y = tk.Entry(self.size_frame, width=10, textvariable=self.input_shape[1])
        self.input_channels = tk.Entry(self.size_frame, width=10, textvariable=self.input_shape[2])
        self.input_x.grid(column=0, row=1)
        self.input_y.grid(column=1, row=1)
        self.input_channels.grid(column=2, row=1)
        self.input_button = tk.Button(self.size_frame, text='Input', command=self.check, width=20)
        self.input_button.grid(column=0, columnspan=3, row=2)

    def check(self):
        print('input:', [i.get() for i in self.input_shape])
        self.manager.forward()

    def __str__(self):
        return ('input_block')

    @property
    def get(self):
        return [i.get() for i in self.input_shape]


class ConfigBlock:
    def __init__(self, manager, root, net_block=None):
        self.manager = manager
        self.root = root
        self.number = 0
        if net_block is None:
            self.net_block_frame = tk.Frame(self.root)
            self.net_block_frame.pack()
        else:
            self.net_block_frame = net_block
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.add_button = tk.Button(self.frame, width=10, text='+', command=self.add_block)
        self.add_button.grid(column=0, columnspan=3, row=0)
        self.shape_label = tk.Label(self.frame, text='output:')
        self.shape_label.grid(column=0, columnspan=3, row=1)
        self.shape_labels = [tk.Label(self.frame) for _ in range(3)]
        [l.grid(column=i, row=2) for i, l in enumerate(self.shape_labels)]

    def add_block(self):
        self.manager.add_block(Block(self.net_block_frame, name=f'block{self.number}'))
        self.number += 1

    def forward(self, x):
        return tuple(x)

    def display_shape(self, shape):
        self.shape_label.config(text=f'output:{str(shape)},total:{shape[0]*shape[1]*shape[2]}')
        #for l,s in zip(self.shape_labels,shape):
        #    l.config(text=s)



if __name__ == '__main__':
    win = tk.Tk()
    Manage(win)
    win.mainloop()
