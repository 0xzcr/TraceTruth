import math
import re
from collections import Counter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtGui import QPen, QPainter, QFont
from PySide6.QtCore import Qt

STOPWORDS = {
    "the", "and", "or", "of", "to", "in", "a", "an", "is", "are", "was", "were",
    "it", "that", "this", "with", "for", "on", "as", "by", "from", "at", "be",
}


def extract_keywords(text, limit=10):
    words = re.findall(r"[A-Za-z]+", text.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    counts = Counter(words)
    return counts.most_common(limit)


def build_edges(sentences, keywords):
    edges = Counter()
    key_set = set(k for k, _ in keywords)
    for sentence in sentences:
        words = set(re.findall(r"[A-Za-z]+", sentence.lower()))
        present = [k for k in key_set if k in words]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                pair = tuple(sorted((present[i], present[j])))
                edges[pair] += 1
    return edges


class MindMapWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

    def update_from_text(self, text):
        self.scene.clear()
        if not text.strip():
            return

        keywords = extract_keywords(text)
        if not keywords:
            return

        sentences = re.split(r"[.!?]", text)
        edges = build_edges(sentences, keywords)

        center_x, center_y = 250, 220
        radius = 170
        positions = {}

        max_count = max(c for _, c in keywords)
        for i, (word, count) in enumerate(keywords):
            angle = (2 * math.pi * i) / len(keywords)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[word] = (x, y, count)

        edge_pen = QPen(Qt.darkGray)
        edge_pen.setWidth(2)
        for (a, b), weight in edges.items():
            if a not in positions or b not in positions:
                continue
            x1, y1, _ = positions[a]
            x2, y2, _ = positions[b]
            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(edge_pen)
            self.scene.addItem(line)

        for word, (x, y, count) in positions.items():
            scale = 0.6 + (count / max_count) * 0.8
            size = 36 * scale
            node = QGraphicsEllipseItem(x - size / 2, y - size / 2, size, size)
            node.setPen(QPen(Qt.black))
            node.setBrush(Qt.white)
            self.scene.addItem(node)

            label = QGraphicsTextItem(word)
            label.setDefaultTextColor(Qt.black)
            label.setFont(QFont("Arial", 10))
            label.setPos(x - (len(word) * 3), y - 10)
            self.scene.addItem(label)
