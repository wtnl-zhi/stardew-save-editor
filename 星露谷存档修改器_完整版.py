
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog,
    QLineEdit, QHBoxLayout, QSpinBox, QListWidget, QMessageBox
)

ITEM_ID_MAP = {
    "金水壶": {"type": "Tool", "id": 273, "level": 3},
    "星之果实": {"type": "Object", "id": 434},
    "传送图腾：农场": {"type": "Object", "id": 688},
    "远古种子": {"type": "Object", "id": 499},
    "铱金锭": {"type": "Object", "id": 337},
}

class StardewEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("星露谷存档修改器")
        self.setGeometry(300, 200, 600, 500)

        layout = QVBoxLayout()

        self.tree = None
        self.root = None
        self.player = None
        self.items_node = None

        # 存档路径
        self.path_input = QLineEdit(self)
        browse_btn = QPushButton("打开存档", self)
        browse_btn.clicked.connect(self.browse_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.path_input)
        file_layout.addWidget(browse_btn)

        # 金钱修改
        self.money_input = QLineEdit(self)
        self.money_input.setPlaceholderText("设置金钱数量")

        # 钓鱼等级修改
        self.fishing_level = QSpinBox(self)
        self.fishing_level.setRange(0, 59)
        self.fishing_level.setPrefix("钓鱼等级：")

        # 添加物品
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("搜索物品")
        self.item_list = QListWidget(self)
        for name in ITEM_ID_MAP:
            self.item_list.addItem(name)

        # 保存按钮
        save_btn = QPushButton("保存修改", self)
        save_btn.clicked.connect(self.save_changes)

        layout.addLayout(file_layout)
        layout.addWidget(QLabel("金钱："))
        layout.addWidget(self.money_input)
        layout.addWidget(self.fishing_level)
        layout.addWidget(QLabel("添加物品（搜索+快捷）："))
        layout.addWidget(self.search_box)
        layout.addWidget(self.item_list)
        layout.addWidget(save_btn)
        self.setLayout(layout)

        self.search_box.textChanged.connect(self.filter_items)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择存档文件", "", "XML Files (*.xml)")
        if file_name:
            self.path_input.setText(file_name)
            self.load_save(file_name)

    def load_save(self, path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.player = self.root.find("player")
        self.items_node = self.player.find("items")
        money = self.player.find("money").text
        self.money_input.setText(money)
        xp = self.player.find("experiencePoints")
        if xp is not None:
            fishing_xp = int(xp.findall("int")[1].text)
            approx_level = min(59, fishing_xp // 250)
            self.fishing_level.setValue(approx_level)

    def save_changes(self):
        if not self.tree:
            QMessageBox.warning(self, "错误", "请先加载存档文件")
            return
        # 修改金钱
        money_node = self.player.find("money")
        money_node.text = self.money_input.text()

        # 修改钓鱼经验
        xp_node = self.player.find("experiencePoints")
        if xp_node is not None:
            xp_node.findall("int")[1].text = str(self.fishing_level.value() * 250)

        # 添加选中物品
        selected = self.item_list.selectedItems()
        for item in selected:
            name = item.text()
            data = ITEM_ID_MAP[name]
            if data["type"] == "Tool":
                tool = ET.Element("Item", attrib={"xsi:type": "Tool"})
                ET.SubElement(tool, "initialParentTileIndex").text = str(data["id"])
                ET.SubElement(tool, "currentParentTileIndex").text = str(data["id"])
                ET.SubElement(tool, "indexOfMenuItemView").text = str(data["id"])
                ET.SubElement(tool, "upgradeLevel").text = str(data["level"])
                ET.SubElement(tool, "instantUse").text = "false"
                ET.SubElement(tool, "numAttachmentSlots").text = "0"
                ET.SubElement(tool, "attachments")
                ET.SubElement(tool, "name").text = name
                self.items_node.append(tool)
            elif data["type"] == "Object":
                obj = ET.Element("Item", attrib={"xsi:type": "Object"})
                ET.SubElement(obj, "parentSheetIndex").text = str(data["id"])
                ET.SubElement(obj, "stack").text = "1"
                ET.SubElement(obj, "name").text = name
                self.items_node.append(obj)

        save_path = self.path_input.text().replace(".xml", "_修改后.xml")
        self.tree.write(save_path, encoding="utf-8", xml_declaration=True)
        QMessageBox.information(self, "成功", f"已保存为：{save_path}")

    def filter_items(self, text):
        self.item_list.clear()
        for name in ITEM_ID_MAP:
            if text.strip() in name:
                self.item_list.addItem(name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = StardewEditor()
    editor.show()
    sys.exit(app.exec_())
