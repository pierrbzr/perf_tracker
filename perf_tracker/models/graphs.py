"""
models/graphs2.py
Toutes les fonctions relatives à la création des graphiques
"""

import pyqtgraph as pg
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

import time
from datetime import datetime

from assets.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_BG_CARD, COLOR_BG_INPUT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_BORDER, COLOR_BORDER_ACTIVE, FONT_FAMILY,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,

)
from models.wellness import get_team_wellness_range_average
from models.rpe import get_team_rpe_range_average


class WellnessChart(QFrame):
    def __init__(self, days: int = 30, parent=None):
        super().__init__(parent)
        self.setObjectName("wellnessChart")
        self.days = days

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # ── Configuration globale pyqtgraph ──
        pg.setConfigOptions(antialias=True)

        # ── Widget graphique ──
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#1E1E2E")
        self.plot_widget.showGrid(x=False, y=False, alpha=0.2)
        self.plot_widget.setYRange(1, 5)
        self.plot_widget.setTitle("Wellness moyen — Équipe", color=f"{COLOR_TEXT_PRIMARY}", size="15pt")
        self.plot_widget.setLabel("left", "Score moyen (/5)", color=f"{COLOR_TEXT_SECONDARY}")

        # Axe X avec dates
        self.axis = pg.DateAxisItem(orientation="bottom")
        self.plot_widget.setAxisItems({"bottom": self.axis})

        # Style des axes
        self.plot_widget.getAxis("left").setTextPen(COLOR_TEXT_SECONDARY)
        self.plot_widget.getAxis("bottom").setTextPen(COLOR_TEXT_SECONDARY)
        self.plot_widget.getAxis("bottom").setTickSpacing(major=86400 * 2, minor=86400)  # ← 1 tick par jour (86400s)

        # ── Label tooltip ──
        self.tooltip_label = QLabel("")
        self.tooltip_label.setAlignment(Qt.AlignCenter)
        self.tooltip_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                background-color: transparent;
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 4px 10px;
                font-size: {FONT_SIZE_BODY}px;
                font-family: "{FONT_FAMILY}";
            }}
        """)
        self.tooltip_label.setVisible(True)

        layout.addWidget(self.plot_widget)
        layout.addWidget(self.tooltip_label)

        self._plot()

    def _plot(self):
        rows = get_team_wellness_range_average(days=self.days)

        if not rows:
            return

        # Conversion des dates en timestamps (requis par DateAxisItem)
        self.dates_str = [r["date"] for r in rows]
        self.scores    = [r["ROUND(AVG(score_total), 2)"] for r in rows]
        self.timestamps = [
            time.mktime(datetime.strptime(d, "%Y-%m-%d").timetuple())
            for d in self.dates_str
        ]
        ticks_majeurs = [
            (ts, datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m"))
            for ts, date in zip(self.timestamps[::2], self.dates_str[::2])
        ]
        self.plot_widget.getAxis("bottom").setTicks([ticks_majeurs, []])

        # ── Ligne de référence à 3.0 ──
        ref_line = pg.InfiniteLine(
            pos=3.0, angle=0,
            pen=pg.mkPen(color=COLOR_TEXT_SECONDARY, width=1, style=Qt.DashLine)
        )
        self.plot_widget.addItem(ref_line)

        # ── Zone remplie sous la courbe ──
        fill = pg.FillBetweenItem(
            pg.PlotDataItem(self.timestamps, self.scores),
            pg.PlotDataItem(self.timestamps, [1] * len(self.scores)),
        )
        self.plot_widget.addItem(fill)

        # ── Courbe principale ──
        self.curve = self.plot_widget.plot(
            self.timestamps, self.scores,
            pen=pg.mkPen(color="#534AB7", width=2),
            symbol="o",
            symbolSize=6,
            symbolBrush="#534AB7",
            symbolPen=pg.mkPen(color="#534AB7")
        )

        # ── Crosshair + tooltip au survol ──
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen("#534AB7", width=1))
        self.plot_widget.addItem(self.vline)
        self.vline.setVisible(False)

        self.proxy = pg.SignalProxy(
            self.plot_widget.scene().sigMouseMoved,
            rateLimit=60,
            slot=self._on_hover
        )

    def _on_hover(self, event):
        
        # Conversion "2025-04-01" → "01 Avril, 2025"
        MOIS = {
            1: "Janvier", 2: "Février",  3: "Mars",      4: "Avril",
            5: "Mai",     6: "Juin",     7: "Juillet",   8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        
        pos = event[0]
        if not self.plot_widget.sceneBoundingRect().contains(pos):
            self.vline.setVisible(False)
            self.tooltip_label.setVisible(False)
            return

        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(pos)
        x = mouse_point.x()

        # Trouve le point le plus proche
        if not self.timestamps:
            return

        closest_idx = min(range(len(self.timestamps)), key=lambda i: abs(self.timestamps[i] - x))

        self.vline.setPos(self.timestamps[closest_idx])
        self.vline.setVisible(True)

        dt = datetime.strptime(self.dates_str[closest_idx], "%Y-%m-%d")
        date_formatee = f"{dt.day:02d} {MOIS[dt.month]}, {dt.year}"

        self.tooltip_label.setText(f"📅 {date_formatee}   |   Score : {self.scores[closest_idx]} / 5")
        self.tooltip_label.setVisible(True)

    def refresh(self, days: int = None):
        if days is not None:
            self.days = days
        self.plot_widget.clear()
        self._plot()
        
    def set_days(self, days: int):
        self.days = days
        self.refresh()
        
class RPEChart(QFrame):
    def __init__(self, days: int = 30, parent=None):
        super().__init__(parent)
        self.setObjectName("RPEChart")
        self.days = days

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # ── Configuration globale pyqtgraph ──
        pg.setConfigOptions(antialias=True)

        # ── Widget graphique ──
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#1E1E2E")
        self.plot_widget.showGrid(x=False, y=False, alpha=0.2)
        self.plot_widget.setYRange(1, 10)
        self.plot_widget.setTitle("RPE moyen — Équipe", color=f"{COLOR_TEXT_PRIMARY}", size="15pt")
        self.plot_widget.setLabel("left", "Score moyen (/10)", color=f"{COLOR_TEXT_SECONDARY}")

        # Axe X avec dates
        self.axis = pg.DateAxisItem(orientation="bottom")
        self.plot_widget.setAxisItems({"bottom": self.axis})

        # Style des axes
        self.plot_widget.getAxis("left").setTextPen(COLOR_TEXT_SECONDARY)
        self.plot_widget.getAxis("bottom").setTextPen(COLOR_TEXT_SECONDARY)
        self.plot_widget.getAxis("bottom").setTickSpacing(major=86400 * 2, minor=86400)  # ← 1 tick par jour (86400s)

        # ── Label tooltip ──
        self.tooltip_label = QLabel("")
        self.tooltip_label.setAlignment(Qt.AlignCenter)
        self.tooltip_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                background-color: transparent;
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 4px 10px;
                font-size: {FONT_SIZE_BODY}px;
                font-family: "{FONT_FAMILY}";
            }}
        """)
        self.tooltip_label.setVisible(True)

        layout.addWidget(self.plot_widget)
        layout.addWidget(self.tooltip_label)

        self._plot()

    def _plot(self):
        rows = get_team_rpe_range_average(days=self.days)

        if not rows:
            return

        # Conversion des dates en timestamps (requis par DateAxisItem)
        self.dates_str = [r["date"] for r in rows]
        self.scores_rpem = [r["ROUND(AVG(rpem), 2)"] for r in rows]
        self.scores_rpec = [r["ROUND(AVG(rpec), 2)"] for r in rows]
        self.timestamps = [
            time.mktime(datetime.strptime(d, "%Y-%m-%d").timetuple())
            for d in self.dates_str
        ]
        ticks_majeurs = [
            (ts, datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m"))
            for ts, date in zip(self.timestamps[::2], self.dates_str[::2])
        ]
        self.plot_widget.getAxis("bottom").setTicks([ticks_majeurs, []])

        # ── Ligne de référence à 5.0 ──
        ref_line = pg.InfiniteLine(
            pos=5.0, angle=0,
            pen=pg.mkPen(color=COLOR_TEXT_SECONDARY, width=1, style=Qt.DashLine)
        )
        self.plot_widget.addItem(ref_line)

        # ── Zone remplie sous la courbe ──
        fill_rpem = pg.FillBetweenItem(
            pg.PlotDataItem(self.timestamps, self.scores_rpem),
            pg.PlotDataItem(self.timestamps, [1] * len(self.scores_rpem)),
        )
        
        fill_rpec = pg.FillBetweenItem(
            pg.PlotDataItem(self.timestamps, self.scores_rpec),
            pg.PlotDataItem(self.timestamps, [1] * len(self.scores_rpec)),
        )
        self.plot_widget.addItem(fill_rpem)
        self.plot_widget.addItem(fill_rpec)

        # ── Courbes principales ──
        self.curve_rpem = self.plot_widget.plot(
            self.timestamps, self.scores_rpem,
            pen=pg.mkPen(color="#E07B54", width=2),
            symbol="o",
            symbolSize=6,
            symbolBrush="#E07B54",
            symbolPen=pg.mkPen(color="#E07B54")
        )
        
        self.curve_rpec = self.plot_widget.plot(
            self.timestamps, self.scores_rpec,
            pen=pg.mkPen(color="#534AB7", width=2),
            symbol="o",
            symbolSize=6,
            symbolBrush="#534AB7",
            symbolPen=pg.mkPen(color="#534AB7")
        )

        # ── Crosshair + tooltip au survol ──
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen("#534AB7", width=1))
        self.plot_widget.addItem(self.vline)
        self.vline.setVisible(False)

        self.proxy = pg.SignalProxy(
            self.plot_widget.scene().sigMouseMoved,
            rateLimit=60,
            slot=self._on_hover
        )

    def _on_hover(self, event):
        
        # Conversion "2025-04-01" → "01 Avril, 2025"
        MOIS = {
            1: "Janvier", 2: "Février",  3: "Mars",      4: "Avril",
            5: "Mai",     6: "Juin",     7: "Juillet",   8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        
        pos = event[0]
        if not self.plot_widget.sceneBoundingRect().contains(pos):
            self.vline.setVisible(False)
            self.tooltip_label.setVisible(False)
            return

        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(pos)
        x = mouse_point.x()

        # Trouve le point le plus proche
        if not self.timestamps:
            return

        closest_idx = min(range(len(self.timestamps)), key=lambda i: abs(self.timestamps[i] - x))

        self.vline.setPos(self.timestamps[closest_idx])
        self.vline.setVisible(True)

        dt = datetime.strptime(self.dates_str[closest_idx], "%Y-%m-%d")
        date_formatee = f"{dt.day:02d} {MOIS[dt.month]}, {dt.year}"

        self.tooltip_label.setText(f"📅 {date_formatee}   |   <font color='#E07B54'>■</font> RPE M : {self.scores_rpem[closest_idx]} / 10   |  <font color='#534AB7'>■</font> RPE C : {self.scores_rpec[closest_idx]} / 10")
        self.tooltip_label.setVisible(True)

    def refresh(self, days: int = None):
        if days is not None:
            self.days = days
        self.plot_widget.clear()
        self._plot()
        
    def set_days(self, days: int):
        self.days = days
        self.refresh()
