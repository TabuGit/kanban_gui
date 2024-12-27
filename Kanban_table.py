from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QInputDialog,
    QTableWidgetItem,
    QMenu,
    QDialog,
    QTextEdit,
    QFileDialog,
    QColorDialog
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import json


class Kanban(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon("table.png"))
        self.setWindowTitle("Kanban table")
        self.setFixedSize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.add_table_button = QPushButton("Add Table")
        self.add_table_button.setFixedSize(150, 40)
        self.add_table_button.clicked.connect(self.add_table)
        
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.setFixedSize(150, 40)
        self.add_task_button.clicked.connect(self.add_task)

        self.save_file_button = QPushButton("Save file")
        self.save_file_button.setFixedSize(150, 40)
        self.save_file_button.clicked.connect(self.save_file)

        self.load_file_button = QPushButton("Load file")
        self.load_file_button.setFixedSize(150, 40)
        self.load_file_button.clicked.connect(self.load_file)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_table_button)
        buttons_layout.addWidget(self.add_task_button)
        buttons_layout.addWidget(self.save_file_button)
        buttons_layout.addWidget(self.load_file_button)

        self.tables_layout = QHBoxLayout()
        self.layout.addLayout(self.tables_layout)
        self.layout.addLayout(buttons_layout)

    def add_table(self):
        table = QTableWidget(0, 1)
        table.setHorizontalHeaderLabels([". . ."])

        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, table))
        
        table_layout = QHBoxLayout()
        table_layout.addWidget(table)
        self.tables_layout.addLayout(table_layout)

    def show_context_menu(self, pos, table):
        context_menu = QMenu(self)

        delete_task = QAction("Delete the task", self)
        delete_task.triggered.connect(lambda: self.delete_task_(table))

        change_member = QAction("Change the member", self)
        change_member.triggered.connect(lambda: self.change_member_(pos, table))
        
        change_header = QAction("Change the table name", self)
        change_header.triggered.connect(lambda: self.change_table_header(table))

        change_height = QAction("Change the height of a cell", self)
        change_height.triggered.connect(lambda: self.change_height_task(pos, table))

        decompose = QAction("Decompose", self)
        decompose.triggered.connect(lambda: self.decompose_func(pos, table))

        set_color = QAction("Set color", self)
        set_color.triggered.connect(lambda: self.set_color_func(table))

        context_menu.addAction(change_height)
        context_menu.addAction(decompose)
        context_menu.addAction(delete_task)
        context_menu.addAction(change_member)
        context_menu.addAction(change_header)
        context_menu.addAction(set_color)

        context_menu.exec(table.mapToGlobal(pos))
    
    def delete_task_(self, table):
        task, ok = QInputDialog.getInt(self, "Deleting the task", "Choose the task id")
        if ok:
            table.removeRow(task)
    
    def change_member_(self, pos, table):
        task = table.rowAt(pos.y())
        new_member, ok = QInputDialog.getText(self, "Changing the member", "Type a name", text='')
        if ok:
            table.setVerticalHeaderItem(task, QTableWidgetItem(new_member))

    def change_table_header(self, table):
        new_header, ok = QInputDialog.getText(self, "Changing the header", "Type new header", text = '. . .')
        if ok:
            table.setHorizontalHeaderItem(0, QTableWidgetItem(new_header))
    
    def change_height_task(self, pos, table):
        task = table.rowAt(pos.y())
        height, ok = QInputDialog.getInt(self, "Changing the height", "Choose the height")
        if ok:
            table.setRowHeight(task, height)

    def add_task(self):
        table_id, ok = QInputDialog.getInt(self, "Adding the task", "Choose table id")
        if ok: 
            the_layout = self.tables_layout.itemAt(table_id).layout()
            table = the_layout.itemAt(0).widget()
            row_count = table.rowCount()
            table.insertRow(row_count)
            table.setItem(row_count, 0, QTableWidgetItem(0))

            

    def decompose_func(self, pos, table):
        task = table.rowAt(pos.y())
        column = 0 
        current_text = table.item(task, column).text() if table.item(task, column).text() else ""
        dialog = QDialog(self)
        dialog.setWindowTitle("Decomposing the task")
        
        text_edit = QTextEdit(dialog)
        text_edit.setPlainText(current_text)
        
        add_item_button = QPushButton("Add item", dialog)
        add_item_button.clicked.connect(lambda: self.add_list_item(text_edit))

        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.save_decompose(table, task, column, text_edit, dialog))
        
        layout = QVBoxLayout(dialog)
        layout.addWidget(text_edit)
        layout.addWidget(add_item_button)
        layout.addWidget(save_button)

        dialog.exec()

    def set_color_func(self, table):
        color = QColorDialog.getColor()
        column_index = 0
        for row in range(table.rowCount()):
            item = table.item(row, column_index)
            if item is not None:
                item.setBackground(color)

    def add_list_item(self, text_edit):
        current_text = text_edit.toPlainText()
        if current_text.strip():
            current_text += "\n• "
            text_edit.setPlainText(current_text)
        
    def save_decompose(self, table, task, column, text_edit, dialog):
        if text_edit.toPlainText().strip():
            table.item(task, column).setText(text_edit.toPlainText())
        dialog.accept()

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Table", "", "JSON files (*.json)")
        if file_name:
            full_data = []
            for table_ in range(self.tables_layout.count()):
                data_to_save = []
                a = self.tables_layout.itemAt(table_).layout()  #in a QVboxlayout
                b = a.itemAt(0).widget()  #in a table
                for row_ in range(b.rowCount()):
                    colomn_name = b.horizontalHeaderItem(0).text()
                    row_names = (b.verticalHeaderItem(row_).text() if b.verticalHeaderItem(row_) is not None else row_+1)
                    row_height = b.rowHeight(row_)
                    row_text = b.item(row_, 0).text()
                    row_color = b.item(row_, 0).background().color().name()
                    data_to_save.append([colomn_name, row_names, row_height, row_text, row_color])
                full_data.append(data_to_save)
            with open(file_name, "w") as f:
                json.dump(full_data, f)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Table", "", "JSON files (*.json)")
        if file_name:
            with open(file_name, "rb") as f:
                data_loaded = json.load(f)
            
            for table_data in data_loaded:
                table = QTableWidget(0, 1)
                table.setHorizontalHeaderItem(0, QTableWidgetItem(table_data[0][0]))
                table.setContextMenuPolicy(Qt.CustomContextMenu)
                table.customContextMenuRequested.connect(lambda pos, t=table: self.show_context_menu(pos, t))
                table_layout = QHBoxLayout()
                table_layout.addWidget(table)
                self.tables_layout.addLayout(table_layout)
                for row_index in range(len(table_data)):
                    row__ = table.rowCount()
                    table.insertRow(row__)
                    table.setItem(row_index, 0, QTableWidgetItem(table_data[row_index][3]))
                    table.setVerticalHeaderItem(row_index, QTableWidgetItem(table_data[row_index][1]))
                    table.setRowHeight(row_index, table_data[row_index][2])
                    table.item(row__, 0).setBackground(QColor(table_data[row_index][4]))

if __name__ == "__main__":
    app = QApplication([])
    window = Kanban()
    window.show()
    app.exec()