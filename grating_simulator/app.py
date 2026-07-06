import os
import time
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QTextEdit, QDialog, QFileDialog, QGroupBox
from PySide6.QtGui import QImage, QPixmap, QWheelEvent, QPainter, QTextCursor
from PySide6.QtCore import Qt

from grating_simulator.ui.main_window_ui import Ui_MainWindow
from grating_simulator.ui.widgets import PopupWindow, ZoomableGraphicsView, TextRedirector

from grating_simulator.simulators.grating import Grating_generator
from grating_simulator.simulators.microscope import Microscope_image_simulator
from grating_simulator.simulators.projection import Projection_image_simulator
from grating_simulator.simulators.scheimpflug import Scheimpflug_simulator
from grating_simulator.simulators.fft_analyzer import FFTImageAnalyzer

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("Initializing...")

        self.session_dir = os.path.join("output", datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.session_dir, exist_ok=True)
        print(f"Output folder: {os.path.abspath(self.session_dir)}")
        # ------------------------------------------------------------------------------------
        # Tab 1
        # ------------------------------------------------------------------------------------

        # 터미널 출력을 위한 QTextEdit 위젯 생성
        self.terminal = self.ui.terminalTextEdit
        self.terminal.setReadOnly(True)
        self.terminal.setLineWrapMode(QTextEdit.NoWrap)

        # 터미널 위젯을 레이아웃에 추가
        self.ui.terminalGroupBox.layout().addWidget(self.terminal)

        # 표준 출력을 터미널 위젯으로 리다이렉트
        sys.stdout = TextRedirector(self.terminal)
        sys.stderr = TextRedirector(self.terminal)

        # GraphicsView를 ZoomableGraphicsView로 교체
        self.ui.graphicsView_ori = ZoomableGraphicsView()
        self.ui.graphicsView_gen = ZoomableGraphicsView()
        self.ui.graphicsView_stack = ZoomableGraphicsView()

        # 레이아웃에 추가
        self.ui.gridLayout_7.addWidget(self.ui.graphicsView_ori)
        self.ui.gridLayout_8.addWidget(self.ui.graphicsView_gen)
        self.ui.gridLayout_9.addWidget(self.ui.graphicsView_stack)

        # Grating generator 인스턴스 생성
        self.grating_generator = Grating_generator()



        # 버튼 시그널 연결
        self.ui.pushButton_3.clicked.connect(self.initialize)
        self.ui.pushButton_4.clicked.connect(self.run)
        self.ui.pushButton_5.clicked.connect(self.show_guide)

        # 파라미터 변경 시그널 연결
        self.connect_parameter_signals()

        # matplotlib 다이얼로그 초기화
        self.dialog_ori = None
        self.dialog_gen = None
        self.dialog_stack = None

        # Save/Load 버튼 시그널 연결
        self.ui.pushButton_save.clicked.connect(self.save_parameters)
        self.ui.pushButton_load.clicked.connect(self.load_parameters)


        # ------------------------------------------------------------------------------------
        # Tab 2
        # ------------------------------------------------------------------------------------

        # MicroscopeImageSimulator 인스턴스 생성
        self.mis = Microscope_image_simulator()

        # 이미지 표시를 위한 ZoomableGraphicsView 인스턴스 생성
        self.ui.loaded_image_view = ZoomableGraphicsView()
        self.ui.OTF_view = ZoomableGraphicsView()
        self.ui.result_image_view = ZoomableGraphicsView()

        # 각 GroupBox에 ZoomableGraphicsView 추가
        self.ui.loadedImageGroupBox.layout().addWidget(self.ui.loaded_image_view)
        self.ui.calcuratedOTFGroupBox.layout().addWidget(self.ui.OTF_view)
        self.ui.resultImageGroupBox.layout().addWidget(self.ui.result_image_view)

        # MicroscopeImageSimulatorTab 초기화
        self.initialize_microscope_simulator_tab()

        # ------------------------------------------------------------------------------------
        # Tab 3
        # ------------------------------------------------------------------------------------

        self.ss = Scheimpflug_simulator()

        self.ui.asw_loaded_image_view = ZoomableGraphicsView()
        self.ui.asw_warped_image_view = ZoomableGraphicsView()
        self.ui.asw_attenuation_view = ZoomableGraphicsView()
        self.ui.asw_final_result_view = ZoomableGraphicsView()
        self.ui.asw_cross_section_view = ZoomableGraphicsView()

        self.ui.prjLoadedImageGroupBox_2.layout().addWidget(self.ui.asw_loaded_image_view)
        self.ui.prjResultProjectedImageGroupBox_2.layout().addWidget(self.ui.asw_warped_image_view)
        self.ui.prjCalcuratedOTFGroupBox_2.layout().addWidget(self.ui.asw_attenuation_view)
        self.ui.prjResultDefocusedImageGroupBox_2.layout().addWidget(self.ui.asw_final_result_view)
        self.ui.prjPSFcrsGroupBox_2.layout().addWidget(self.ui.asw_cross_section_view)

        self.initialize_scheimpflug_tab()

        # ------------------------------------------------------------------------------------
        # Tab 4
        # ------------------------------------------------------------------------------------

        # MicroscopeImageSimulator 인스턴스 생성
        self.pis = Projection_image_simulator()

        # 이미지 표시를 위한 ZoomableGraphicsView 인스턴스 생성
        self.ui.prj_loaded_image_view = ZoomableGraphicsView()
        self.ui.prj_OTF_view = ZoomableGraphicsView()
        self.ui.prj_projected_image_view = ZoomableGraphicsView()
        self.ui.prj_defocused_image_view = ZoomableGraphicsView()
        self.ui.prj_PSFcrs_view = ZoomableGraphicsView()


        # 각 GroupBox에 ZoomableGraphicsView 추가
        self.ui.prjLoadedImageGroupBox.layout().addWidget(self.ui.prj_loaded_image_view)
        self.ui.prjCalcuratedOTFGroupBox.layout().addWidget(self.ui.prj_OTF_view)
        self.ui.prjResultProjectedImageGroupBox.layout().addWidget(self.ui.prj_projected_image_view)
        self.ui.prjResultDefocusedImageGroupBox.layout().addWidget(self.ui.prj_defocused_image_view)
        self.ui.prjPSFcrsGroupBox.layout().addWidget(self.ui.prj_PSFcrs_view)


        # MicroscopeImageSimulatorTab 초기화
        self.initialize_projection_image_simulator_tab()

        # ------------------------------------------------------------------------------------
        # Tab 5 (FFT Image Analysis)
        # ------------------------------------------------------------------------------------

        self.fft_analyzer = FFTImageAnalyzer()
        self._create_fft_tab_ui()
        self._connect_fft_signals()

        print("Initialization complete.")

    def display_image(self, graphics_view, img, normalize=True,  dheight=1, dwidth=1):
        """이미지를 graphics_view에 표시"""
        # 이미지 전처리
        if normalize:
            img = img.astype(np.float32)
            img /= np.max(img)
            img *= 255
            img = img.astype(np.uint8)
        else:
            img = img.astype(np.uint8)

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # QGraphicsView로 표시
        height, width = img.shape[:2]
        bytes_per_line = 3 * width

        # QImage 생성
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        if dheight != dwidth:
            # 물리적 크기 비율 계산
            aspect_ratio = (dwidth * width) / (dheight * height)

            # 정사각형으로 만들기 위해 더 큰 쪽을 기준으로 스케일링
            if aspect_ratio > 1:
                # 너비가 더 큰 경우
                new_height = int(width / aspect_ratio)
                pixmap = pixmap.scaled(width, new_height) #, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                # 높이가 더 큰 경우
                new_width = int(height * aspect_ratio)
                pixmap = pixmap.scaled(new_width, height) #, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        scene = QGraphicsScene(self)
        scene.addPixmap(pixmap)
        graphics_view.setScene(scene)
        graphics_view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
        graphics_view.setAlignment(Qt.AlignCenter)

    '''
    Tab 1-----------------------------------------------------------------------------------------------------------
    '''
    def connect_parameter_signals(self):
        """파라미터 입력 위젯들의 시그널을 연결"""
        # General Parameters
        self.ui.headerLineEdit.textChanged.connect(self.update_parameters)
        self.ui.samplingPixelSizeUmDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.invertReusltCheckBox.stateChanged.connect(self.update_parameters)

        # Grating Parameters
        self.ui.periodOfPatternUmDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.heightOfSawtoothUmDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.periodOfSawtoothUmDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.widthOfStemUmDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.offsetBtwLinesDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.numOfLinesSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.lengthOfLineUmDoubleSpinBox.valueChanged.connect(self.update_parameters)

        # Advanced Parameters
        self.ui.diameterOfEdgeOfSawtoothUmDoubleSpinBox.valueChanged.connect(self.update_parameters)
        self.ui.methodComboBox.currentIndexChanged.connect(self.update_parameters)
        self.ui.factorSpinBox.valueChanged.connect(self.update_parameters)

    def update_parameters(self):
        """UI의 현재 상태를 Grating_generator의 파라미터로 업데이트"""
        # General Parameters
        self.grating_generator.gt_id = self.ui.headerLineEdit.text()
        self.grating_generator.mask_sampling_width_in_um = self.ui.samplingPixelSizeUmDoubleSpinBox.value()
        self.grating_generator.invert_result = self.ui.invertReusltCheckBox.isChecked()

        # Grating Parameters
        self.grating_generator.period_pattern = self.ui.periodOfPatternUmDoubleSpinBox.value()
        self.grating_generator.amplitude_of_saw = self.ui.heightOfSawtoothUmDoubleSpinBox.value()
        self.grating_generator.period_of_saw = self.ui.periodOfSawtoothUmDoubleSpinBox.value()
        self.grating_generator.width_of_stem = self.ui.widthOfStemUmDoubleSpinBox.value()
        self.grating_generator.offset_btw_pattern = self.ui.offsetBtwLinesDoubleSpinBox.value()
        self.grating_generator.number_of_pattern = self.ui.numOfLinesSpinBox.value()
        self.grating_generator.length_of_grating_in_um = self.ui.lengthOfLineUmDoubleSpinBox.value()

        # Advanced Parameters
        self.grating_generator.diameter_of_edge_of_saw_in_um = self.ui.diameterOfEdgeOfSawtoothUmDoubleSpinBox.value()
        self.grating_generator.mask_rounding = True

        # Method ComboBox 처리
        method_index = self.ui.methodComboBox.currentIndex()
        if method_index == 0:
            self.grating_generator.round_size_px = 'AUTO'
        elif method_index == 1:
            self.grating_generator.round_size_px = None
        else:
            self.grating_generator.round_size_px = 'User'
            self.grating_generator.round_size_px_user = self.ui.factorSpinBox.value()

        # 파라미터 일관성 체크
        self.check_parameter_consistency()


    def check_parameter_consistency(self):
        """파라미터 일관성을 체크하고 결과를 표시"""
        try:
            self.grating_generator.check_parameter_consistency()
            self.ui.parameterConsistencyCheckLineEdit.setText("Pass")
            self.ui.parameterConsistencyCheckLineEdit.setStyleSheet("background-color: #90EE90;")  # 연한 초록색
        except AssertionError as e:
            self.ui.parameterConsistencyCheckLineEdit.setText("Fail")
            self.ui.parameterConsistencyCheckLineEdit.setStyleSheet("background-color: #FFB6C1;")  # 연한 빨간색
            print(f"Error: {str(e)}")

    def initialize(self):
        """초기화 버튼 클릭 시 실행"""
        print("Updating...")
        self.update_parameters()
        print("\t-> update complete.\n")

    def update_plots(self):
        """결과 이미지를 업데이트"""
        # Original mask plot
        self.display_image(self.ui.graphicsView_ori, self.grating_generator.mask_ori)

        # Generated mask plot
        self.display_image(self.ui.graphicsView_gen, self.grating_generator.mask_gen)

        # Stacked mask plot
        self.display_image(self.ui.graphicsView_stack, self.grating_generator.buffer)

    def run(self):
        """실행 버튼 클릭 시 실행"""
        print("Running grating generation...")
        self.update_parameters()
        self.grating_generator.run()

        self.update_plots()  # 결과 이미지 업데이트

        print("Grating generation complete.")
        if self.ui.saveCheckBox.isChecked():
            json_path = os.path.join(self.session_dir, self.ui.headerLineEdit.text() + 'Grating_params.json')
            self.save_parameters(input_path=json_path)
            self.grating_generator.save_grating(output_dir=self.session_dir)
        self.update_review_parameters()


    def update_review_parameters(self):
        # review parameter
        self.ui.imageHeightPxLineEdit.setText(str(self.grating_generator.H))
        self.ui.imageWidthPxLineEdit.setText(str(self.grating_generator.W))

        # mm 단위로 변환하여 소수점 둘째 자리까지 표시
        height_mm = self.grating_generator.H * self.grating_generator.mask_sampling_width_in_um / 1000
        width_mm = self.grating_generator.W * self.grating_generator.mask_sampling_width_in_um / 1000

        self.ui.imageHeightMmLineEdit.setText(f"{height_mm:.2f}")
        self.ui.imageWidthMmLineEdit.setText(f"{width_mm:.2f}")

        # 스타일 설정
        self.ui.imageHeightPxLineEdit.setStyleSheet("background-color: #aaffff;")
        self.ui.imageWidthPxLineEdit.setStyleSheet("background-color: #aaffff;")
        self.ui.imageHeightMmLineEdit.setStyleSheet("background-color: #aaffff;")
        self.ui.imageWidthMmLineEdit.setStyleSheet("background-color: #aaffff;")

    def show_guide(self):
        """파라미터 가이드 다이어그램을 PopupWindow에 표시"""
        fig = self._create_guide_figure()
        self.ui.pop_ZGV = ZoomableGraphicsView()
        self.popup_window = PopupWindow()
        self.popup_window.layout.addWidget(self.ui.pop_ZGV)
        self.popup_window.display_matplotlib_fig(self.ui.pop_ZGV, fig)
        self.popup_window.show()
        plt.close(fig)

    def _create_guide_figure(self):
        """현재 파라미터 값을 사용하여 격자 형상 가이드 다이어그램 생성"""
        fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')

        amp = self.grating_generator.amplitude_of_saw
        T = self.grating_generator.period_of_saw
        stem = self.grating_generator.width_of_stem
        offset = self.grating_generator.offset_btw_pattern
        edge_d = self.grating_generator.diameter_of_edge_of_saw_in_um
        period = 2 * amp + stem + offset

        # Triangle wave for 4 sawtooth periods
        n_saw = 4
        x = np.linspace(0, n_saw * T, 2000)
        tri = np.abs(2 * ((x / T) - np.floor(x / T + 0.5)))

        # Pattern boundary: stem center at yc, bottom of pattern at y=0
        yc = amp + stem / 2
        def pattern_edges(tri_val, y_center):
            upper = amp * tri_val + stem / 2 + y_center
            lower = amp * (tri_val - 1) - stem / 2 + y_center
            return upper, lower

        u1, l1 = pattern_edges(tri, yc)
        u2, l2 = pattern_edges(tri, yc - period)

        # Draw patterns
        fill_kw = dict(color='#4488cc', alpha=0.3, edgecolor='#1155aa', linewidth=1.8)
        ax.fill_between(x, l1, u1, **fill_kw)
        ax.fill_between(x, l2, u2, **fill_kw)

        # Stem reference lines
        ax.axhline(amp + stem, color='#999', ls=':', lw=0.7, zorder=0)
        ax.axhline(amp, color='#999', ls=':', lw=0.7, zorder=0)

        # Key Y coordinates
        y_top = 2 * amp + stem
        y_st = amp + stem
        y_sb = amp
        y_bot = 0
        y_gap_bot = -offset

        # Annotation colors
        C_saw = '#cc2222'
        C_amp = '#008800'
        C_stem = '#cc8800'
        C_off = '#8800cc'
        C_per = '#0066cc'
        C_edge = '#555555'

        xL = -n_saw * T * 0.15
        xR = n_saw * T * 1.15

        # Vertical dimension line helper
        def dimv(xp, y1, y2, text, color, side):
            ax.annotate('', xy=(xp, y2), xytext=(xp, y1),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
            my = (y1 + y2) / 2
            ha = 'right' if side == 'left' else 'left'
            dx = -n_saw * T * 0.02 if side == 'left' else n_saw * T * 0.02
            ax.text(xp + dx, my, text, ha=ha, va='center', fontsize=9, color=color,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, alpha=0.9))

        # Horizontal dimension line helper
        def dimh(yp, x1, x2, text, color):
            ax.annotate('', xy=(x2, yp), xytext=(x1, yp),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
            mx = (x1 + x2) / 2
            ax.text(mx, yp + amp * 0.15, text, ha='center', va='bottom', fontsize=9,
                    color=color, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, alpha=0.9))

        # Leader line helper
        def leader(x1, y1, x2, y2, color):
            ax.plot([x1, x2], [y1, y2], color=color, lw=0.5, ls=':')

        # --- Annotations ---

        # 1. period_of_saw (horizontal, above pattern)
        yp = y_top + amp * 0.5
        dimh(yp, T / 2, 3 * T / 2, f'period_of_saw = {T} µm', C_saw)
        leader(T / 2, y_top, T / 2, yp, C_saw)
        leader(3 * T / 2, y_top, 3 * T / 2, yp, C_saw)

        # 2. amplitude_of_saw upper (left)
        dimv(xL, y_st, y_top, f'amplitude_of_saw\n= {amp} µm', C_amp, 'left')
        leader(xL, y_top, T / 2, y_top, C_amp)
        leader(xL, y_st, 0, y_st, C_amp)

        # 3. width_of_stem (left)
        dimv(xL, y_sb, y_st, f'width_of_stem\n= {stem} µm', C_stem, 'left')
        leader(xL, y_sb, 0, y_sb, C_stem)

        # 4. amplitude_of_saw lower (left, abbreviated)
        dimv(xL, y_bot, y_sb, f'(= {amp} µm)', C_amp, 'left')
        leader(xL, y_bot, 0, y_bot, C_amp)

        # 5. offset_btw_pattern (right, in gap)
        x_off = xR - n_saw * T * 0.08
        dimv(x_off, y_gap_bot, y_bot, f'offset_btw_pattern\n= {offset} µm', C_off, 'right')

        # 6. period_pattern (far right)
        dimv(xR, y_gap_bot, y_top, f'period_pattern\n= {period:.2f} µm', C_per, 'right')
        leader(T / 2, y_top, xR, y_top, C_per)
        leader(0, y_gap_bot, xR, y_gap_bot, C_per)

        # 7. diameter_of_edge_of_saw (callout at peak)
        peak_x, peak_y = T / 2, y_top
        ax.annotate(f'diameter_of_edge_of_saw\n= {edge_d} µm',
                    xy=(peak_x, peak_y),
                    xytext=(peak_x + T * 1.5, peak_y + amp * 0.8),
                    fontsize=9, color=C_edge, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=C_edge, alpha=0.9),
                    arrowprops=dict(arrowstyle='->', color=C_edge, lw=1.2,
                                   connectionstyle='arc3,rad=0.2'))

        # Formatting
        ax.set_xlim(xL - n_saw * T * 0.2, xR + n_saw * T * 0.2)
        ax.set_ylim(-period - amp * 0.5, y_top + amp * 1.5)
        ax.set_xlabel('X direction (along grating teeth) [µm]', fontsize=10)
        ax.set_ylabel('Y direction (stacking / period direction) [µm]', fontsize=10)
        ax.set_title('Grating Parameter Guide  (current values)', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.15)
        fig.tight_layout()
        return fig


    def save_parameters(self, input_path = False):
        """현재 파라미터를 JSON 파일로 저장"""
        import json

        params = {
            # General Parameters
            'gt_id': self.ui.headerLineEdit.text(),
            'mask_sampling_width_in_um': self.ui.samplingPixelSizeUmDoubleSpinBox.value(),
            'invert_result': self.ui.invertReusltCheckBox.isChecked(),

            # Grating Parameters
            'period_pattern': self.ui.periodOfPatternUmDoubleSpinBox.value(),
            'amplitude_of_saw': self.ui.heightOfSawtoothUmDoubleSpinBox.value(),
            'period_of_saw': self.ui.periodOfSawtoothUmDoubleSpinBox.value(),
            'width_of_stem': self.ui.widthOfStemUmDoubleSpinBox.value(),
            'offset_btw_pattern': self.ui.offsetBtwLinesDoubleSpinBox.value(),
            'number_of_pattern': self.ui.numOfLinesSpinBox.value(),
            'length_of_grating_in_um': self.ui.lengthOfLineUmDoubleSpinBox.value(),

            # Advanced Parameters
            'diameter_of_edge_of_saw_in_um': self.ui.diameterOfEdgeOfSawtoothUmDoubleSpinBox.value(),
            'method_index': self.ui.methodComboBox.currentIndex(),
            '-> AUTO':0,
            '-> None':1,
            '-> User':2,
            '-->User rounding factor': self.ui.factorSpinBox.value(),

        }
        if input_path == False:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Parameters", self.session_dir,
                "JSON Files (*.json);;All Files (*)"
            )

            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        json.dump(params, f, indent=4)
                    print(f"Parameters saved to {file_path}")
                except Exception as e:
                    print(f"Error saving parameters: {str(e)}")
        else:
            try:
                with open(input_path, 'w') as f:
                    json.dump(params, f, indent=4)
                print(f"Parameters saved to {input_path}")
            except Exception as e:
                print(f"Error saving parameters: {str(e)}")


    def load_parameters(self):
        """JSON 파일에서 파라미터 불러오기"""
        import json

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Parameters", self.session_dir,
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    params = json.load(f)

                # General Parameters
                self.ui.headerLineEdit.setText(params['gt_id'])
                self.ui.samplingPixelSizeUmDoubleSpinBox.setValue(params['mask_sampling_width_in_um'])
                self.ui.invertReusltCheckBox.setChecked(params['invert_result'])

                # Grating Parameters
                self.ui.periodOfPatternUmDoubleSpinBox.setValue(params['period_pattern'])
                self.ui.heightOfSawtoothUmDoubleSpinBox.setValue(params['amplitude_of_saw'])
                self.ui.periodOfSawtoothUmDoubleSpinBox.setValue(params['period_of_saw'])
                self.ui.widthOfStemUmDoubleSpinBox.setValue(params['width_of_stem'])
                self.ui.offsetBtwLinesDoubleSpinBox.setValue(params['offset_btw_pattern'])
                self.ui.numOfLinesSpinBox.setValue(params['number_of_pattern'])
                self.ui.lengthOfLineUmDoubleSpinBox.setValue(params['length_of_grating_in_um'])

                # Advanced Parameters
                self.ui.diameterOfEdgeOfSawtoothUmDoubleSpinBox.setValue(params['diameter_of_edge_of_saw_in_um'])
                self.ui.methodComboBox.setCurrentIndex(params['method_index'])
                self.ui.factorSpinBox.setValue(params['factor'])

                # 파라미터 업데이트
                self.update_parameters()
                print(f"Parameters loaded from {file_path}")

            except Exception as e:
                print(f"Error loading parameters: {str(e)}")
    '''
    Tab 2-----------------------------------------------------------------------------------------------------------
    '''
    def initialize_microscope_simulator_tab(self):
        """MicroscopeImageSimulatorTab 초기화 및 시그널 연결"""

        # 이미지 로드 버튼 연결
        self.ui.loadGratingPushButton.clicked.connect(self.load_microscope_image)
        self.ui.loadGratingParamsPushButton.clicked.connect(self.load_grating_parameters)
        # 버튼 시그널 연결
        self.ui.initializePushButton.clicked.connect(self.init_connect_parameter)
        # 계산 버튼
        self.ui.OTFPushButton.clicked.connect(self.calculate_OTF)
        self.ui.RunPushButton.clicked.connect(self.generate_microscope_image)

    def load_microscope_image(self):
        """이미지 로드"""
        print("loading image...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", self.session_dir, "Image Files (*.bmp *.png *.jpg)"
        )
        if file_path:
            self.mis.load_image(file_path)

            # heightPxLineEdit 업데이트
            self.ui.heightPxLineEdit.setText(str(self.mis.H))
            self.ui.widthPxLineEdit.setText(str(self.mis.W))

            self.ui.heightPxLineEdit.setStyleSheet("background-color: #aaffff;")
            self.ui.widthPxLineEdit.setStyleSheet("background-color: #aaffff;")


            self.display_image(self.ui.loaded_image_view, self.mis.mask_bmp, normalize=False)
            print("\t-> image loaded.\n")


    def load_grating_parameters(self):
        """그레이팅 파라미터 로드"""
        print("loading grating parameters...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Parameters", self.session_dir, "JSON Files (*.json)"
        )
        if file_path:
            self.mis.load_grating_parameters(file_path)
            # samplingSizeUmDoubleSpinBox 업데이트
            self.ui.samplingSizeUmDoubleSpinBox.setValue(self.mis.mask_sampling_width_in_um)
            self.ui.samplingSizeUmDoubleSpinBox.setStyleSheet("background-color: #aaffff;")

            self.ui.heightMmLineEdit.setText(f"{self.mis.H*self.mis.mask_sampling_width_in_um/1000:.2f}")
            self.ui.widthMmLineEdit.setText(f"{self.mis.W*self.mis.mask_sampling_width_in_um/1000:.2f}")
            self.ui.heightMmLineEdit.setStyleSheet("background-color: #aaffff;")
            self.ui.widthMmLineEdit.setStyleSheet("background-color: #aaffff;")
            print("\t-> grating parameters loaded.\n")

    def init_connect_parameter(self):
        # 파라미터 시그널 연결
        print("initializing microscope simulator...")
        self.connect_microscope_parameter_signals()
        self.update_microscope_parameters()
        print("\t-> microscope simulator initialized.\n")

    def connect_microscope_parameter_signals(self):
        """MicroscopeImageSimulatorTab의 파라미터 시그널 연결"""
        # General Parameters
        self.ui.headerLineEdit_2.textChanged.connect(self.update_microscope_parameters)
        self.ui.nAOfOpticsDoubleSpinBox.valueChanged.connect(self.update_microscope_parameters)

        # Spectrum Parameters
        self.ui.spectrumMinUmDoubleSpinBox.valueChanged.connect(self.update_microscope_parameters)
        self.ui.spectrumMaxUmDoubleSpinBox.valueChanged.connect(self.update_microscope_parameters)
        self.ui.spectrumStepDoubleSpinBox.valueChanged.connect(self.update_microscope_parameters)

        # Image Parameters
        self.ui.samplingSizeUmDoubleSpinBox.valueChanged.connect(self.update_microscope_parameters)
        self.ui.heightPxLineEdit.textChanged.connect(self.update_microscope_parameters)
        self.ui.widthPxLineEdit.textChanged.connect(self.update_microscope_parameters)

    def update_microscope_parameters(self):
        """UI의 현재 상태를 MicroscopeImageSimulator의 파라미터로 업데이트"""
        # General Parameters
        self.mis.microscope_id = self.ui.headerLineEdit_2.text()
        self.mis.NA = self.ui.nAOfOpticsDoubleSpinBox.value()

        # Spectrum Parameters
        self.mis.custom_spectrum = self.ui.customSpectrumGroupBox.isChecked()
        if self.mis.custom_spectrum:
            self.mis.set_user_spectrum(
                self.ui.spectrumMinUmDoubleSpinBox.value(),
                self.ui.spectrumMaxUmDoubleSpinBox.value(),
                self.ui.spectrumStepDoubleSpinBox.value()
            )
        else:
            self.mis.wvls = [0.5876]  # 기본값

        self.mis.mask_sampling_width_in_um = self.ui.samplingSizeUmDoubleSpinBox.value()
        self.mis.H = int(self.ui.heightPxLineEdit.text())
        self.mis.W = int(self.ui.widthPxLineEdit.text())

        # initialize optics and grid
        self.mis.initialize_optics()
        # 파라미터 일관성 체크
        self.check_microscope_parameter_consistency()

    def check_microscope_parameter_consistency(self):
        """MicroscopeImageSimulator 파라미터 일관성 체크"""
        try:
            self.mis.check_simulation_condition()
            self.ui.simulationConditionLineEdit.setText("Pass")
            self.ui.simulationConditionLineEdit.setStyleSheet("background-color: #90EE90;")
            self.ui.nAOfOpticsDoubleSpinBox.setStyleSheet("background-color: #90EE90;")
            self.ui.samplingSizeUmDoubleSpinBox.setStyleSheet("background-color: #90EE90;")
        except AssertionError as e:
            self.ui.simulationConditionLineEdit.setText("Fail")
            self.ui.simulationConditionLineEdit.setStyleSheet("background-color: #FFB6C1;")
            self.ui.nAOfOpticsDoubleSpinBox.setStyleSheet("background-color: #FFB6C1;")
            print(f"Error: {str(e)}")



    def calculate_OTF(self):
        """OTF 계산"""
        print("calculating OTF...")
        self.mis.initialize_optics()
        self.mis.calculate_OTF()
        dky = self.mis.dky
        dkx = self.mis.dkx
        ratio = dky/dkx
        self.display_image(self.ui.OTF_view, self.mis.eff_OTF_uint, normalize=False,
                           dheight=1, dwidth=1/ratio)
        print("\t-> OTF calculated.\n")

    def generate_microscope_image(self):
        """현미경 이미지 생성"""
        print("generating microscope image...")
        self.mis.perform_OTF()
        self.display_image(self.ui.result_image_view, self.mis.imaged_gt_uint, normalize=False)
        print("\t-> microscope image generated.\n")
        if self.ui.saveCheckBox.isChecked():
            self.mis.save_image(output_dir=self.session_dir)

    '''
    Tab 4-----------------------------------------------------------------------------------------------------------
    '''


    def initialize_projection_image_simulator_tab(self):
        """MicroscopeImageSimulatorTab 초기화 및 시그널 연결"""

        # 이미지 로드 버튼 연결
        self.ui.prjLoadGratingPushButton.clicked.connect(self.prj_load_image)
        self.ui.prjLoadGratingParamsPushButton.clicked.connect(self.prj_load_image_parameters)
        # 버튼 시그널 연결
        self.ui.prjAutoInitializeCheckBox.clicked.connect(self.prj_connect_parameter_signals)
        self.ui.prjInitializePushButton.clicked.connect(self.prj_init_connect_parameter)

        # 계산 버튼
        self.ui.prjOTFPushButton.clicked.connect(self.prj_calculate_OTF)
        self.ui.prjRunPushButton.clicked.connect(self.prj_generate_projected_image)
        self.ui.prjPSFcrsPushButton.clicked.connect(self.prj_create_PSFcrs)
        self.ui.prjPlotImageCrsPushButton.clicked.connect(self.prj_plot_image_crs)
        self.ui.prjPlotPSFCrspushButton.clicked.connect(self.prj_plot_PSFcrs)
        self.ui.prjPushButton_save.clicked.connect(self.prj_save_parameters)
        self.ui.prjPushButton_load.clicked.connect(self.prj_load_parameters)

    def prj_load_image(self):
        """이미지 로드"""
        print("loading image...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", self.session_dir, "Image Files (*.bmp *.png *.jpg)"
        )
        if file_path:
            self.pis.load_image(file_path)

            # heightPxLineEdit 업데이트
            self.ui.prjHeightPxLineEdit.setText(str(self.pis.H))
            self.ui.prjWidthPxLineEdit.setText(str(self.pis.W))

            self.ui.prjHeightPxLineEdit.setStyleSheet("background-color: #aaffff;")
            self.ui.prjWidthPxLineEdit.setStyleSheet("background-color: #aaffff;")


            self.display_image(self.ui.prj_loaded_image_view, self.pis.mask_bmp, normalize=False)
            print("\t-> image loaded.\n")


    def prj_load_image_parameters(self):
        """그레이팅 파라미터 로드"""
        print("loading grating parameters...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Parameters", self.session_dir, "JSON Files (*.json)"
        )
        if file_path:
            self.pis.load_grating_parameters(file_path)
            # samplingSizeUmDoubleSpinBox 업데이트
            self.ui.prjSamplingSizeUmDoubleSpinBox.setValue(self.pis.mask_sampling_width_in_um)
            self.ui.prjSamplingSizeUmDoubleSpinBox.setStyleSheet("background-color: #aaffff;")
            self.ui.prjPeriodOfSawDoubleSpinBox.setValue(self.pis.period_of_saw)
            self.ui.prjPeriodOfSawDoubleSpinBox.setStyleSheet("background-color: #aaffff;")

            self.ui.prjHeightMmLineEdit.setText(f"{self.pis.H*self.pis.mask_sampling_width_in_um/1000:.2f}")
            self.ui.prjWidthMmLineEdit.setText(f"{self.pis.W*self.pis.mask_sampling_width_in_um/1000:.2f}")
            self.ui.prjHeightMmLineEdit.setStyleSheet("background-color: #aaffff;")
            self.ui.prjWidthMmLineEdit.setStyleSheet("background-color: #aaffff;")
            print("\t-> grating parameters loaded.\n")

    def prj_init_connect_parameter(self):
        # 파라미터 시그널 연결
        print("initializing microscope simulator...")
        self.prj_connect_parameter_signals()
        print("\t-> projection simulator connected.\n")
        self.prj_update_parameters()


    def prj_connect_parameter_signals(self):
        """MicroscopeImageSimulatorTab의 파라미터 시그널 연결 또는 해제"""
        # 시그널 연결 상태를 추적하는 속성이 없다면 초기화
        if not hasattr(self, '_signals_connected'):
            self._signals_connected = False

        if self.ui.prjAutoInitializeCheckBox.isChecked() and not self._signals_connected:
            # 시그널 연결
            self.ui.prjHeaderPrefixLineEdit.textChanged.connect(self.prj_update_parameters)

            # Spectrum Parameters
            self.ui.prjSpectrumMinUmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjSpectrumMaxUmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjSpectrumStepDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)

            # Projection Parameters
            self.ui.prjZ0GratingToLensMmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjZ1LensToProjectionPlaneMmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjPupilDiameterMmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjDefocusMmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjResizeFactorPixelBinningDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjEdgeRemoverGroupBox.toggled.connect(self.prj_update_parameters)
            self.ui.prjEdgeRemoverFactorDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)

            # Grating Parameters
            self.ui.prjPeriodOfSawDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self.ui.prjSamplingSizeUmDoubleSpinBox.valueChanged.connect(self.prj_update_parameters)
            self._signals_connected = True
            print("Auto-update enabled: Parameters will update automatically when changed")
        elif not self.ui.prjAutoInitializeCheckBox.isChecked() and self._signals_connected:
            # 시그널 연결 해제
            try:
                self.ui.prjHeaderPrefixLineEdit.textChanged.disconnect(self.prj_update_parameters)

                # Spectrum Parameters
                self.ui.prjSpectrumMinUmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjSpectrumMaxUmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjSpectrumStepDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)

                # Projection Parameters
                self.ui.prjZ0GratingToLensMmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjZ1LensToProjectionPlaneMmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjPupilDiameterMmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjDefocusMmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjResizeFactorPixelBinningDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjEdgeRemoverGroupBox.toggled.disconnect(self.prj_update_parameters)
                self.ui.prjEdgeRemoverFactorDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)

                # Grating Parameters
                self.ui.prjPeriodOfSawDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)
                self.ui.prjSamplingSizeUmDoubleSpinBox.valueChanged.disconnect(self.prj_update_parameters)

            except TypeError:
                # 이미 연결이 해제되었거나 연결되지 않은 경우
                pass
            self._signals_connected = False
            print("Auto-update disabled: Use 'Initialize' button to update parameters")

    def prj_update_parameters(self):
        """UI의 현재 상태를 MicroscopeImageSimulator의 파라미터로 업데이트"""
        # 즉시 출력을 위해 flush=True 사용
        print("\nupdating parameters...\n...\n...\n...", flush=True)

        # GUI 이벤트 처리를 강제로 실행하여 출력이 즉시 표시되도록 함
        QApplication.processEvents()

        # General Parameters
        self.pis.header_prefix = self.ui.prjHeaderPrefixLineEdit.text()
        self.pis.z0_mm = self.ui.prjZ0GratingToLensMmDoubleSpinBox.value()
        self.pis.z1_mm = self.ui.prjZ1LensToProjectionPlaneMmDoubleSpinBox.value()
        self.pis.pupil_diameter_mm = self.ui.prjPupilDiameterMmDoubleSpinBox.value()
        self.pis.defocus_z1_mm = self.ui.prjDefocusMmDoubleSpinBox.value()
        self.pis.resize_factor = self.ui.prjResizeFactorPixelBinningDoubleSpinBox.value()
        self.pis.resize_factor_along_width = self.ui.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.value()
        self.pis.clear_board_toggle = self.ui.prjEdgeRemoverGroupBox.isChecked()
        self.pis.clear_board_factor = self.ui.prjEdgeRemoverFactorDoubleSpinBox.value()

        # Spectrum Parameters
        self.pis.custom_spectrum = self.ui.prjCustomSpectrumGroupBox.isChecked()
        if self.pis.custom_spectrum:
            self.pis.set_user_spectrum(
                self.ui.prjSpectrumMinUmDoubleSpinBox.value(),
                self.ui.prjSpectrumMaxUmDoubleSpinBox.value(),
                self.ui.prjSpectrumStepDoubleSpinBox.value()
            )
        else:
            self.pis.wvls = [0.5876]  # 기본값

        self.pis.mask_sampling_width_in_um = self.ui.prjSamplingSizeUmDoubleSpinBox.value()
        self.pis.period_of_saw = self.ui.prjPeriodOfSawDoubleSpinBox.value()
        self.pis.H = int(self.ui.prjHeightPxLineEdit.text())
        self.pis.W = int(self.ui.prjWidthPxLineEdit.text())

        # initialize optics and grid
        self.pis.initialize_optics()
        # 파라미터 일관성 체크
        self.prj_check_parameter_consistency()
        self.prj_update_review_parameters()
        print('============================================')
        print('============================================')
        print("** Projection simulator updated. **")
        print('============================================')
        print('============================================')

    def prj_check_parameter_consistency(self):
        """MicroscopeImageSimulator 파라미터 일관성 체크"""
        try:
            self.pis.check_simulation_condition()
            self.ui.prjSimulationConditionLineEdit.setText("Pass")
            self.ui.prjSimulationConditionLineEdit.setStyleSheet("background-color: #90EE90;")
            self.ui.prjPupilDiameterMmDoubleSpinBox.setStyleSheet("background-color: #90EE90;")
            self.ui.prjZ0GratingToLensMmDoubleSpinBox.setStyleSheet("background-color: #90EE90;")
            self.ui.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setStyleSheet("background-color: #90EE90;")
        except AssertionError as e:
            self.ui.prjSimulationConditionLineEdit.setText("Fail")
            self.ui.prjSimulationConditionLineEdit.setStyleSheet("background-color: #FFB6C1;")
            self.ui.prjPupilDiameterMmDoubleSpinBox.setStyleSheet("background-color: #FFB6C1;")
            self.ui.prjZ0GratingToLensMmDoubleSpinBox.setStyleSheet("background-color: #FFB6C1;")
            self.ui.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setStyleSheet("background-color: #FFB6C1;")
            print(f"Error: {str(e)}")

    def prj_update_review_parameters(self):
        """review parameter"""
        self.ui.prjObjectSpaceFLineEdit.setText(f"{self.pis.obj_space_f_number:.4f}")
        self.ui.prjImageSpaceNALineEdit.setText(f"{self.pis.img_space_na:.4f}")
        self.ui.prjMagnificationLineEdit.setText(f"{self.pis.magnification_defo:.4f}")
        self.ui.prjFullDepthOfFieldMmLineEdit.setText(f"{self.pis.DOF_bidirec_mm:.2f}")
        self.ui.prjProjectedImageHeightMmLineEdit.setText(f"{self.pis.projection_H_mm:.2f} mm ({self.pis.H} px)")
        self.ui.prjProjectedImageWidthMmLineEdit.setText(f"{self.pis.projection_W_mm:.2f} mm ({self.pis.W} px)")
        self.ui.prjProjectedImageSamplingSizeUmLineEdit.setText(f"{self.pis.projection_sampling_width_in_um:.6f}")
        self.ui.prjResizedImageHeightMmLineEdit.setText(f"{self.pis.resized_H_mm:.2f} mm ({self.pis.resized_H} px)")
        self.ui.prjResizedImageWidthMmLineEdit.setText(f"{self.pis.resized_W_mm:.2f} mm ({self.pis.resized_W} px)")
        self.ui.prjResizedImageSamplingSizeUmLineEdit.setText(f"{self.pis.resized_sampling_width_in_um:.4f}")

        self.ui.prjObjectSpaceFLineEdit.setStyleSheet("background-color: #fffddd;")
        self.ui.prjImageSpaceNALineEdit.setStyleSheet("background-color: #cccccc;")
        self.ui.prjMagnificationLineEdit.setStyleSheet("background-color: #fffddd;")
        self.ui.prjFullDepthOfFieldMmLineEdit.setStyleSheet("background-color: #fffddd;")
        self.ui.prjProjectedImageHeightMmLineEdit.setStyleSheet("background-color: #cccccc;")
        self.ui.prjProjectedImageWidthMmLineEdit.setStyleSheet("background-color: #cccccc;")
        self.ui.prjProjectedImageSamplingSizeUmLineEdit.setStyleSheet("background-color: #cccccc;")
        self.ui.prjResizedImageHeightMmLineEdit.setStyleSheet("background-color: #cccccc;")
        self.ui.prjResizedImageWidthMmLineEdit.setStyleSheet("background-color: #cccccc;")
        self.ui.prjResizedImageSamplingSizeUmLineEdit.setStyleSheet("background-color: #fffddd;")



    def prj_calculate_OTF(self):
        """OTF 계산"""
        print("calculating OTF...")
        self.pis.initialize_optics()
        self.pis.calculate_OTF()
        dky = self.pis.dky
        dkx = self.pis.dkx
        ratio = dky/dkx

        self.display_image(self.ui.prj_OTF_view, self.pis.eff_defocus_OTF_uint,
                           normalize=False, dheight=1, dwidth=1/ratio)
        print("\t-> OTF calculated.\n")

    def prj_generate_projected_image(self):
        """프로젝션 이미지 생성"""
        print("generating microscope image...")
        try:
            self.pis.perform_OTF()
            self.pis.resize_result()
            self.display_image(self.ui.prj_projected_image_view, self.pis.resized_result_uint, normalize=False)
            self.display_image(self.ui.prj_defocused_image_view, self.pis.resized_defocused_result_uint, normalize=False)
            if self.ui.prjSaveResultCheckBox.isChecked():
                self.pis.save_image(output_dir=self.session_dir)
                json_path = os.path.join(self.session_dir, self.pis.header_prefix + 'Projection_params.json')
                self.prj_save_parameters(input_path=json_path)
            print("\t-> microscope image generated.\n")
        except Exception as e:
            print(f"Error: {str(e)}")

    def prj_create_PSFcrs(self):
        """PSF 생성"""
        print("creating PSF...")
        print("** It may take a while... **")

        # GUI 업데이트를 위한 잠시 대기
        QApplication.processEvents()

        time.sleep(0.1)
        self.pis.check_psf_prop()
        H,W = self.pis.psf_crs_uint.shape[:2]
        self.display_image(self.ui.prj_PSFcrs_view, self.pis.psf_crs_uint, normalize=False,
                           dheight=1, dwidth=H/W) # set image ratio to squre
        print("\t-> PSF created.\n")

    def prj_plot_image_crs(self):
        fig = self.pis.plot_matplotlib_image_crs()

        save_path = os.path.join(self.session_dir, self.pis.header_prefix + 'image_cross_section.png')
        fig.savefig(save_path, dpi=150)
        print(f"Cross-section plot saved to {save_path}")

        self.ui.pop_ZGV = ZoomableGraphicsView()
        self.popup_window = PopupWindow()
        self.popup_window.layout.addWidget(self.ui.pop_ZGV)
        self.popup_window.display_matplotlib_fig(self.ui.pop_ZGV, fig)
        self.popup_window.show()

    def prj_plot_PSFcrs(self):
        fig = self.pis.plot_matplotlib_psf_crs()

        self.ui.pop_ZGV = ZoomableGraphicsView()
        self.popup_window = PopupWindow()
        self.popup_window.layout.addWidget(self.ui.pop_ZGV)
        self.popup_window.display_matplotlib_fig(self.ui.pop_ZGV, fig)
        self.popup_window.show()

    def prj_save_parameters(self, input_path = False):
        """현재 파라미터를 JSON 파일로 저장"""
        self.prj_update_parameters()

        if input_path == False:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Parameters", self.session_dir,
                "JSON Files (*.json);;All Files (*)"
            )
            if file_path:
                try:
                    self.pis.save_parameters_json_dict(file_path)
                except Exception as e:
                    print(f"Error saving parameters: {str(e)}")
        else:
            try:
                self.pis.save_parameters_json_dict(input_path)
            except Exception as e:
                print(f"Error saving parameters: {str(e)}")


    def prj_load_parameters(self):
        """JSON 파일에서 파라미터 불러오기"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Parameters", self.session_dir,
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                self.pis.update_parameters_json_dict(file_path)

                # General Parameters
                self.ui.prjHeaderPrefixLineEdit.setText(self.pis.header_prefix)
                # projection parameter
                self.ui.prjZ0GratingToLensMmDoubleSpinBox.setValue(self.pis.z0_mm)
                self.ui.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setValue(self.pis.z1_mm)
                self.ui.prjPupilDiameterMmDoubleSpinBox.setValue(self.pis.pupil_diameter_mm)
                self.ui.prjDefocusMmDoubleSpinBox.setValue(self.pis.defocus_z1_mm)
                self.ui.prjResizeFactorPixelBinningDoubleSpinBox.setValue(self.pis.resize_factor)
                self.ui.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.setValue(self.pis.resize_factor_along_width)
                # projection + clear boarder
                self.ui.prjEdgeRemoverGroupBox.setChecked(self.pis.clear_board_toggle)
                self.ui.prjEdgeRemoverFactorDoubleSpinBox.setValue(self.pis.clear_board_factor)
                # custom image property parameters
                self.ui.prjCustomImagePropertyGroupBox.setChecked(self.pis.custom_image_property_toggle)
                self.ui.prjSamplingSizeUmDoubleSpinBox.setValue(self.pis.mask_sampling_width_in_um)
                self.ui.prjPeriodOfSawDoubleSpinBox.setValue(self.pis.period_of_saw)
                # custom spectrum parameters
                self.ui.prjCustomSpectrumGroupBox.setChecked(self.pis.custom_spectrum_toggle)
                self.ui.prjSpectrumMinUmDoubleSpinBox.setValue(self.pis.spectrum_min)
                self.ui.prjSpectrumMaxUmDoubleSpinBox.setValue(self.pis.spectrum_max)
                self.ui.prjSpectrumStepDoubleSpinBox.setValue(self.pis.spectrum_step)

                # 파라미터 업데이트
                self.update_parameters()
                print(f"Parameters loaded from {file_path}")

            except Exception as e:
                print(f"Error loading parameters: {str(e)}")

    '''
    Tab 3-----------------------------------------------------------------------------------------------------------
    '''
    def initialize_scheimpflug_tab(self):
        self.ui.aswLoadProjectedFlatImagePushButton.clicked.connect(self.asw_load_image)
        self.ui.aswLoadProjectorParamsPushButton.clicked.connect(self.asw_load_params)
        self.ui.aswInitializePushButton.clicked.connect(self.asw_initialize)

        self.ui.prjOTFPushButton_2.setText("4. Apply Homography")
        self.ui.prjRunPushButton_2.setText("5. Compute Brightness")
        self.ui.prjPlotImageCrsPushButton_2.setText("6. Plot CrossSection")
        self.ui.prjOTFPushButton_2.clicked.connect(self.asw_apply_homography)
        self.ui.prjRunPushButton_2.clicked.connect(self.asw_compute_attenuation)
        self.ui.prjPlotImageCrsPushButton_2.clicked.connect(self.asw_plot_cross_section)

        self.ui.prjPSFcrsPushButton_2.setVisible(False)
        self.ui.prjPlotPSFCrspushButton_2.setVisible(False)

        self.ui.prjCalcuratedOTFGroupBox_2.setTitle("Brightness Attenuation")
        self.ui.prjResultProjectedImageGroupBox_2.setTitle("Warped Image")
        self.ui.prjResultDefocusedImageGroupBox_2.setTitle("Final Result")
        self.ui.prjPSFcrsGroupBox_2.setTitle("Cross Section")

        self.ui.prjPushButton_save_2.clicked.connect(self.asw_save_parameters)
        self.ui.prjPushButton_load_2.clicked.connect(self.asw_load_parameters)

    def asw_load_image(self):
        print("loading image for Scheimpflug...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Projected Flat Image", self.session_dir, "Image Files (*.bmp *.png *.jpg)")
        if file_path:
            from grating_simulator.simulators.scheimpflug import stretch_image_to_square
            self.ss.load_image(file_path)
            stretch = self.ui.stretchImageToSquareLineEdit.text().strip().lower()
            if stretch in ('true', '1', 'yes'):
                self.ss.proj_image_float = stretch_image_to_square(self.ss.proj_image_float)
                self.ss.proj_image_bmp = self.ss.proj_image_float.astype(np.uint8)
                self.ss.H, self.ss.W = self.ss.proj_image_float.shape[:2]

            self.ui.prjHeightPxLineEdit_2.setText(str(self.ss.H))
            self.ui.prjWidthPxLineEdit_2.setText(str(self.ss.W))
            self.display_image(self.ui.asw_loaded_image_view, self.ss.proj_image_bmp, normalize=False)
            print("\t-> image loaded.\n")

    def asw_load_params(self):
        print("loading projection parameters...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Projection Parameters", self.session_dir, "JSON Files (*.json)")
        if file_path:
            self.ss.load_proj_image_parameters(file_path)
            z1_w_defocus = self.ss.z1_mm + self.ss.defocus_z1_mm
            self.ui.z1WDefocusLensToPlaneMmLineEdit.setText(f"{z1_w_defocus:.2f}")
            self.ui.z0GratingToLensMmLineEdit.setText(f"{self.ss.z0_mm:.2f}")
            self.ui.z1LensToProjectionPlaneMmLineEdit.setText(f"{self.ss.z1_mm:.2f}")
            self.ui.defocusMmLineEdit_2.setText(f"{self.ss.defocus_z1_mm:.2f}")

            if hasattr(self.ss, 'resized_sampling_width_in_um'):
                self.ui.prjSamplingSizeUmDoubleSpinBox_2.setValue(self.ss.resized_sampling_width_in_um)
                pixel_mm = self.ss.resized_sampling_width_in_um / 1000
                self.ui.prjHeightMmLineEdit_2.setText(f"{self.ss.H * pixel_mm:.2f}")
                self.ui.prjWidthMmLineEdit_2.setText(f"{self.ss.W * pixel_mm:.2f}")
            print("\t-> projection parameters loaded.\n")

    def asw_initialize(self):
        print("initializing Scheimpflug simulator...")
        self.ss.x_rot_deg = self.ui.xProjectionAngleDegDoubleSpinBox.value()
        self.ss.y_rot_deg = self.ui.yProjectionAngleDegDoubleSpinBox.value()
        self.ss.header_prefix = self.ui.prjHeaderPrefixLineEdit_2.text()

        if self.ui.prjEdgeRemoverGroupBox_2.isChecked():
            self.ss.pad = int(self.ui.prjEdgeRemoverFactorDoubleSpinBox_2.value())
        else:
            self.ss.pad = 0

        self.ss.initialize_optics()
        self.ss.check_simulation_condition()

        mag = self.ss.magnification
        object_x_angle = -np.rad2deg(np.arctan(np.tan(np.deg2rad(self.ss.x_rot_deg)) / mag))
        object_y_angle = -np.rad2deg(np.arctan(np.tan(np.deg2rad(self.ss.y_rot_deg)) / mag))
        self.ui.xGratingTiltAngleDegLineEdit.setText(f"{object_x_angle:.4f}")
        self.ui.yGratingTiltAngleDegLineEdit.setText(f"{object_y_angle:.4f}")
        print("\t-> Scheimpflug simulator initialized.\n")

    def asw_apply_homography(self):
        print("applying homography...")
        self.ss.apply_homography()
        self.display_image(self.ui.asw_warped_image_view, self.ss.warped_image, normalize=True)
        print("\t-> homography applied.\n")

    def asw_compute_attenuation(self):
        print("computing brightness attenuation...")
        print("** This may take a while (GPU computation)... **")
        QApplication.processEvents()

        self.ss.compute_pixel_to_camera_distance_and_scale_gpu()
        self.ss.final_result = self.ss.inv_sqr_raw * self.ss.warped_image

        attenuation_display = (self.ss.inv_sqr_raw / np.max(self.ss.inv_sqr_raw) * 255).astype(np.uint8)
        self.display_image(self.ui.asw_attenuation_view, attenuation_display, normalize=False)
        self.display_image(self.ui.asw_final_result_view, self.ss.final_result, normalize=True)

        if self.ui.prjSaveResultCheckBox_2.isChecked():
            self.ss.save_image(output_dir=self.session_dir)
            json_path = os.path.join(self.session_dir, self.ss.header_prefix + 'Scheimpflug_params.json')
            self.ss.save_parameters_json_dict(json_path)
        print("\t-> brightness attenuation computed.\n")

    def asw_plot_cross_section(self):
        fig = self.ss.imshow_result()

        save_path = os.path.join(self.session_dir, self.ss.header_prefix + 'scheimpflug_cross_section.png')
        fig.savefig(save_path, dpi=150)
        print(f"Cross-section plot saved to {save_path}")

        self.ui.pop_ZGV = ZoomableGraphicsView()
        self.popup_window = PopupWindow()
        self.popup_window.layout.addWidget(self.ui.pop_ZGV)
        self.popup_window.display_matplotlib_fig(self.ui.pop_ZGV, fig)
        self.popup_window.show()
        plt.close(fig)

    def asw_save_parameters(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Parameters", self.session_dir, "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.ss.save_parameters_json_dict(file_path)

    def asw_load_parameters(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Parameters", self.session_dir, "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.ss.update_parameters_json_dict(file_path)
            self.ui.xProjectionAngleDegDoubleSpinBox.setValue(self.ss.x_rot_deg)
            self.ui.yProjectionAngleDegDoubleSpinBox.setValue(self.ss.y_rot_deg)
            if hasattr(self.ss, 'pad'):
                self.ui.prjEdgeRemoverFactorDoubleSpinBox_2.setValue(float(self.ss.pad))
            print(f"Parameters loaded from {file_path}")

    '''
    Tab 5 (FFT Image Analysis)------------------------------------------------------------------
    '''
    def _create_fft_tab_ui(self):
        from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QGroupBox, QGridLayout, QFormLayout,
            QLineEdit, QDoubleSpinBox, QSizePolicy, QSpacerItem)

        tab = QWidget()
        tab.setObjectName("tab_fft")
        main_layout = QVBoxLayout(tab)

        btn_layout = QHBoxLayout()
        self.ui.fftLoadImageBtn = QPushButton("1. Load Image (*.bmp)")
        self.ui.fftAutoDetectBtn = QPushButton("2. Auto-Detect Angle")
        self.ui.fftAnalyzeBtn = QPushButton("3. Analyze && Plot")
        self.ui.fftSaveFigBtn = QPushButton("4. Save Figure")
        btn_layout.addWidget(self.ui.fftLoadImageBtn)
        btn_layout.addWidget(self.ui.fftAutoDetectBtn)
        btn_layout.addWidget(self.ui.fftAnalyzeBtn)
        btn_layout.addWidget(self.ui.fftSaveFigBtn)
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(btn_layout)

        params_group = QGroupBox("Parameters")
        params_layout = QFormLayout()

        self.ui.fftDetectedAngleLineEdit = QLineEdit()
        self.ui.fftDetectedAngleLineEdit.setReadOnly(True)
        self.ui.fftDetectedAngleLineEdit.setPlaceholderText("Click 'Auto-Detect'")
        params_layout.addRow("Detected angle [deg]:", self.ui.fftDetectedAngleLineEdit)

        self.ui.fftManualAngleSpinBox = QDoubleSpinBox()
        self.ui.fftManualAngleSpinBox.setRange(-180.0, 180.0)
        self.ui.fftManualAngleSpinBox.setDecimals(2)
        self.ui.fftManualAngleSpinBox.setValue(0.0)
        params_layout.addRow("Manual angle [deg]:", self.ui.fftManualAngleSpinBox)

        self.ui.fftPixelSizeSpinBox = QDoubleSpinBox()
        self.ui.fftPixelSizeSpinBox.setRange(0.01, 10000.0)
        self.ui.fftPixelSizeSpinBox.setDecimals(4)
        self.ui.fftPixelSizeSpinBox.setValue(20.0)
        params_layout.addRow("Pixel size [um]:", self.ui.fftPixelSizeSpinBox)

        self.ui.fftImageSizeLineEdit = QLineEdit()
        self.ui.fftImageSizeLineEdit.setReadOnly(True)
        params_layout.addRow("Image size [H x W px]:", self.ui.fftImageSizeLineEdit)

        params_group.setLayout(params_layout)
        main_layout.addWidget(params_group)

        img_layout = QGridLayout()
        orig_group = QGroupBox("Original Image")
        orig_group_layout = QGridLayout(orig_group)
        self.ui.fft_original_view = ZoomableGraphicsView()
        orig_group_layout.addWidget(self.ui.fft_original_view)

        rotated_group = QGroupBox("Rotated Image")
        rotated_group_layout = QGridLayout(rotated_group)
        self.ui.fft_rotated_view = ZoomableGraphicsView()
        rotated_group_layout.addWidget(self.ui.fft_rotated_view)

        img_layout.addWidget(orig_group, 0, 0)
        img_layout.addWidget(rotated_group, 0, 1)
        main_layout.addLayout(img_layout)

        self.ui.tabWidget.addTab(tab, "FFT Image Analysis")

    def _connect_fft_signals(self):
        self.ui.fftLoadImageBtn.clicked.connect(self.fft_load_image)
        self.ui.fftAutoDetectBtn.clicked.connect(self.fft_auto_detect)
        self.ui.fftAnalyzeBtn.clicked.connect(self.fft_analyze)
        self.ui.fftSaveFigBtn.clicked.connect(self.fft_save_figure)

    def fft_load_image(self):
        print("loading image for FFT analysis...")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", self.session_dir, "Image Files (*.bmp *.png *.jpg)")
        if file_path:
            self.fft_analyzer.load_image(file_path)
            self.ui.fftImageSizeLineEdit.setText(f"{self.fft_analyzer.H} x {self.fft_analyzer.W}")
            self.display_image(self.ui.fft_original_view, self.fft_analyzer.img, normalize=False)
            print(f"\t-> image loaded ({self.fft_analyzer.H} x {self.fft_analyzer.W}).\n")

    def fft_auto_detect(self):
        if self.fft_analyzer.img is None:
            print("Error: Load an image first.")
            return
        print("detecting sine wave direction...")
        angle = self.fft_analyzer.analyze_sine_direction()
        self.ui.fftDetectedAngleLineEdit.setText(f"{angle:.3f}")
        self.ui.fftDetectedAngleLineEdit.setStyleSheet("background-color: #90EE90;")
        self.ui.fftManualAngleSpinBox.setValue(angle)
        print(f"\t-> detected angle: {angle:.3f} deg\n")

    def fft_analyze(self):
        if self.fft_analyzer.img is None:
            print("Error: Load an image first.")
            return

        manual_angle = self.ui.fftManualAngleSpinBox.value()
        pixel_size = self.ui.fftPixelSizeSpinBox.value()

        print(f"analyzing at angle {manual_angle:.3f} deg...")
        self.fft_analyzer.rotate_and_extract(angle_deg=manual_angle)

        self.display_image(self.ui.fft_rotated_view, self.fft_analyzer.rotated_img, normalize=False)

        self._fft_fig = self.fft_analyzer.plot_analysis(pixel_size_um=pixel_size)

        self.ui.pop_ZGV = ZoomableGraphicsView()
        self.popup_window = PopupWindow()
        self.popup_window.layout.addWidget(self.ui.pop_ZGV)
        self.popup_window.display_matplotlib_fig(self.ui.pop_ZGV, self._fft_fig)
        self.popup_window.show()
        print("\t-> analysis complete.\n")

    def fft_save_figure(self):
        if not hasattr(self, '_fft_fig') or self._fft_fig is None:
            print("Error: Run analysis first.")
            return
        save_path = os.path.join(self.session_dir, 'fft_analysis.png')
        self._fft_fig.savefig(save_path, dpi=150)
        print(f"FFT analysis figure saved to {save_path}")
