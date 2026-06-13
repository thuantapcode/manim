"""
main.py — Manim animation: "Training LLMs in Academia: Challenge or Calling?"
Target duration: ~7 minutes
Run all 3 scenes as separate videos: python main.py
Or render one scene: manim -pql main.py <SceneName>
"""

from manim import *
import numpy as np
import os
import subprocess
import sys

# Part 4 and Part 5 live beside this file in the GitHub project folder.
PARTS_DIR = os.path.dirname(os.path.abspath(__file__))
if PARTS_DIR not in sys.path:
    sys.path.insert(0, PARTS_DIR)

PARTS_IMPORT_ERROR = None
try:
    from part4 import P4_Complete
    from part5 import P5_Complete
except ModuleNotFoundError as exc:
    P4_Complete = None
    P5_Complete = None
    PARTS_IMPORT_ERROR = exc

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# Bảng màu thống nhất — 3 màu accent chính + 2 neutral
# ─────────────────────────────────────────────────────────────────────────────
# PRIMARY   : BLUE   #3B82F6  →  nội dung học thuật / chủ đạo
# SECONDARY : AMBER  #F59E0B  →  nổi bật / câu hỏi / kết quả
# DANGER    : ROSE   #F43F5E  →  công nghiệp / rào cản / cảnh báo
# NEUTRAL   : SLATE  #94A3B8  →  đường kẻ / label phụ
# SURFACE   : #1E293B          →  nền panel tối
# TEXT      : #F1F5F9          →  chữ chính
#
# Quy tắc:
#  • Mỗi scene chỉ dùng tối đa 3 màu accent cùng lúc
#  • Tất cả FadeIn/FadeOut dùng smooth_step (cubic ease)
#  • run_time ngắn nhất = 0.5s, dài nhất = 2.5s — không vượt
#  • Spacing nhất quán: buff=0.35 giữa các element trong cùng nhóm
# ─────────────────────────────────────────────────────────────────────────────

BLUE   = "#3B82F6"
AMBER  = "#F59E0B"
ROSE   = "#F43F5E"
SLATE  = "#94A3B8"
TEAL   = "#2DD4BF"
SURFACE = "#1E293B"
TEXT    = "#F1F5F9"
MUTED   = "#64748B"
BG      = "#0F172A"

# Compatibility with Scene 4 & 5
ACCENT_BLUE   = BLUE
ACCENT_GREEN  = TEAL
ACCENT_RED    = ROSE
ACCENT_GOLD   = AMBER
ACCENT_CYAN   = TEAL
PANEL_COLOR   = SURFACE
TEXT_GRAY     = MUTED
TEXT_WHITE    = TEXT

# Custom rate function mapping
from manim.utils.rate_functions import ease_out_bounce
smooth_step_in_out = smooth
bounce = ease_out_bounce


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 1 — INTRO  (≈ 1 phút 40 giây)
# ═════════════════════════════════════════════════════════════════════════════
class S1_Intro(Scene):
    # ── helper ───────────────────────────────────────────────────────────────
    def _t(self, text, size=28, color=TEXT, bold=False):
        return Text(text, font="Arial", font_size=size, color=color,
                    weight=BOLD if bold else NORMAL)

    def _panel(self, w, h, accent=BLUE):
        return RoundedRectangle(
            corner_radius=0.14, width=w, height=h,
            fill_color=SURFACE, fill_opacity=0.95,
            stroke_color=accent, stroke_width=2.5
        )

    def _pill(self, label, accent=BLUE):
        txt = self._t(label, size=22, color=accent, bold=True)
        rect = RoundedRectangle(corner_radius=0.22,
                                width=max(txt.width + 0.5, 1.25),
                                height=0.72,
                                fill_color=SURFACE, fill_opacity=1,
                                stroke_color=accent, stroke_width=2)
        txt.move_to(rect)
        return VGroup(rect, txt)

    # ── construct ─────────────────────────────────────────────────────────────
    def construct(self):
        s0_voiceover = [
            ("assets/audio/s0_00_models.mp3",           0.0),
            ("assets/audio/s0_01_power.mp3",           10.8),
            ("assets/audio/s0_02_open_api.mp3",        14.6),
            ("assets/audio/s0_03_industry.mp3",        32.4),
            ("assets/audio/s0_04_university_question.mp3", 45.4),
            ("assets/audio/s0_05_lecture.mp3",         52.7),
            ("assets/audio/s0_06_reports.mp3",         74.1),
            ("assets/audio/s0_07_redaction.mp3",       86.4),
            ("assets/audio/s0_08_rare_papers.mp3",     94.2),
            ("assets/audio/s0_09_aspiration.mp3",     105.6),
            ("assets/audio/s0_10_compute_barrier.mp3",116.9),
        ]
        for p, t in s0_voiceover:
            self.add_sound(p, time_offset=t)

        # ── [00:00 – 00:10.8] Các mô hình lần lượt hiện ra ──────────────────
        model_names = ["GPT", "Claude", "Gemini", "DeepSeek", "Llama", "Qwen"]
        # Mỗi tên dùng pill riêng → nhìn rõ ràng hơn plain text
        pills = VGroup(*[self._pill(n) for n in model_names])
        pills.arrange(RIGHT, buff=0.16).move_to(ORIGIN)
        if pills.width > config.frame_width - 1.0:
            pills.scale_to_fit_width(config.frame_width - 1.0)

        self.play(
            LaggedStart(*[FadeIn(p, shift=UP*0.3, rate_func=smooth_step_in_out)
                          for p in pills],
                        lag_ratio=0.22),
            run_time=2.5
        )
        self.wait(1.5)
        # Thu nhỏ nhẹ + nhích lại gần → cảm giác "tụ lại"
        self.play(pills.animate.arrange(RIGHT, buff=0.08).scale(0.78).move_to(ORIGIN),
                  rate_func=smooth_step_in_out, run_time=1.5)
        self.wait(5.3)

        # ── [00:10.8 – 00:14.6] Sức mạnh bùng nổ ────────────────────────────
        pulse = Circle(radius=0.5, fill_color=ROSE, fill_opacity=0.88,
                       stroke_color=ROSE, stroke_width=0)
        ring  = Circle(radius=0.5, fill_opacity=0, stroke_color=ROSE,
                       stroke_width=2.5)
        self.play(FadeOut(pills, rate_func=smooth_step_in_out, run_time=0.6),
                  FadeIn(pulse, scale=0.25, rate_func=smooth_step_in_out,
                         run_time=0.6))
        self.play(
            pulse.animate.scale(2.6).set_opacity(0),
            ring.animate.scale(3.8).set_stroke(opacity=0),
            rate_func=rush_from,   # ease-out: mulch tăng tốc ở đầu
            run_time=1.5
        )
        self.remove(pulse, ring)

        # Đường phân chia dọc
        divider = Line(UP*3.0, DOWN*3.0, color=SLATE, stroke_width=1.5,
                       stroke_opacity=0.5)
        self.play(Create(divider, rate_func=smooth_step_in_out), run_time=0.7)
        self.wait(3.3)

        # ── [00:14.6 – 00:32.4] Mã nguồn mở vs API ──────────────────────────
        # Dùng icon-box thống nhất với _panel()
        def _side_card(label, accent, direction):
            panel = self._panel(3.6, 2.2, accent)
            icon  = Square(side_length=0.7, fill_color=accent, fill_opacity=0.2,
                           stroke_color=accent, stroke_width=1.5)
            lbl   = self._t(label, size=22, color=accent, bold=True)
            content = VGroup(icon, lbl).arrange(DOWN, buff=0.25)
            content.move_to(panel)
            return VGroup(panel, content).shift(direction * 3.2)

        open_card = _side_card("MÃ NGUỒN MỞ",  TEAL, LEFT)
        api_card  = _side_card("API THƯƠNG MẠI", ROSE, RIGHT)

        self.play(
            FadeIn(open_card, shift=LEFT*0.4,  rate_func=smooth_step_in_out),
            FadeIn(api_card,  shift=RIGHT*0.4, rate_func=smooth_step_in_out),
            run_time=1.5
        )
        self.wait(15.5)
        self.play(FadeOut(VGroup(divider, open_card, api_card),
                          rate_func=smooth_step_in_out), run_time=0.8)

        # ── [00:32.4 – 00:45.4] Khối công nghiệp ────────────────────────────
        industry = self._industry_block().move_to(ORIGIN)
        self.play(FadeIn(industry, scale=0.88, rate_func=smooth_step_in_out),
                  run_time=1.5)
        # GPU flicker — chỉ 2 lần (ngắn gọn, không gây khó chịu)
        gpu_sq = industry[2]
        for _ in range(2):
            self.play(gpu_sq.animate.set_opacity(0.2), run_time=0.2)
            self.play(gpu_sq.animate.set_opacity(1.0), run_time=0.2)
        self.wait(6.5)
        self.play(industry.animate.scale(0.40).to_corner(UR, buff=0.5),
                  rate_func=smooth_step_in_out, run_time=1.2)
        self.wait(3.0)

        # ── [00:45.4 – 00:52.7] Đại học ─────────────────────────────────────
        uni_circle = Circle(radius=0.68, fill_color=BLUE, fill_opacity=0.75,
                            stroke_color=TEAL, stroke_width=2.5)
        uni_circle.to_corner(DL, buff=1.4)
        uni_lbl  = self._t("ĐẠI HỌC", size=22, color=TEXT, bold=True).move_to(uni_circle)
        question = self._t("?", size=68, color=AMBER, bold=True).next_to(uni_circle, UP, buff=0.2)
        uni_grp  = VGroup(uni_circle, uni_lbl)

        self.play(FadeIn(uni_grp, scale=0.6, rate_func=smooth_step_in_out), run_time=0.9)
        self.play(FadeIn(question, shift=DOWN*0.15,
                         rate_func=smooth_step_in_out), run_time=0.6)
        self.wait(3.0)
        self.play(FadeOut(VGroup(industry, question),
                          rate_func=smooth_step_in_out), run_time=0.8)
        # Phóng to mờ dần → hậu cảnh
        self.play(
            FadeOut(uni_lbl, rate_func=smooth_step_in_out),
            uni_circle.animate.scale(9).move_to(ORIGIN)
            .set_fill(opacity=0.045).set_stroke(opacity=0),
            rate_func=smooth_step_in_out, run_time=2.0
        )

        # ── [00:52.7 – 01:14.1] Bài giảng phụ thuộc công nghiệp ─────────────
        board = self._panel(8.2, 4.0, BLUE)
        board.set_fill(color="#0D1B2A", opacity=0.96)
        lecture = self._t("BÀI GIẢNG", size=44, color=BLUE, bold=True).move_to(board)
        # Mũi tên từ góc phải trên → tiêu đề (biểu thị phụ thuộc công nghiệp)
        arrow = Arrow(start=RIGHT*5.8 + UP*2.0, end=lecture.get_right() + RIGHT*0.05,
                      color=ROSE, stroke_width=7, buff=0,
                      tip_length=0.28)
        classroom = VGroup(board, lecture)

        self.play(FadeIn(board, rate_func=smooth_step_in_out),
                  Write(lecture, rate_func=smooth_step_in_out), run_time=1.8)
        self.play(GrowArrow(arrow), run_time=1.2)
        self.wait(17.5)
        self.play(FadeOut(VGroup(classroom, arrow, uni_circle),
                          rate_func=smooth_step_in_out), run_time=0.9)

        # ── [01:14.1 – 01:26.4] Bài báo KH vs Báo cáo DN ────────────────────
        paper_card  = self._label_panel("BÀI BÁO\nKHOA HỌC",   TEAL ).shift(LEFT*3.2)
        report_card = self._label_panel("BÁO CÁO\nDOANH NGHIỆP", ROSE).shift(RIGHT*3.2)

        self.play(
            FadeIn(paper_card,  shift=LEFT*0.3,  rate_func=smooth_step_in_out),
            FadeIn(report_card, shift=RIGHT*0.3, rate_func=smooth_step_in_out),
            run_time=1.2
        )
        self.wait(9.9)
        self.play(
            FadeOut(paper_card, rate_func=smooth_step_in_out),
            report_card.animate.move_to(UP*0.8),
            rate_func=smooth_step_in_out,
            run_time=1.2
        )

        # ── [01:26.4 – 01:34.2] Báo cáo bị che ──────────────────────────────
        lines = VGroup(*[
            Line(LEFT*1.7, RIGHT*1.7, color=SLATE, stroke_width=3.5)
            for _ in range(5)
        ]).arrange(DOWN, buff=0.27).next_to(report_card, DOWN, buff=0.4)

        redact_bars = VGroup(*[
            Rectangle(width=3.4, height=0.18,
                      fill_color=BG, fill_opacity=1,
                      stroke_width=0).move_to(line)
            for line in lines
        ])

        self.play(Create(lines), run_time=0.9)
        self.play(
            LaggedStart(*[FadeIn(b, rate_func=smooth_step_in_out)
                          for b in redact_bars],
                        lag_ratio=0.2),
            run_time=1.0
        )
        self.wait(5.0)
        self.play(FadeOut(VGroup(report_card, lines, redact_bars),
                          rate_func=smooth_step_in_out), run_time=0.9)

        # ── [01:34.2 – 01:45.6] Bài báo minh bạch hiếm hoi ──────────────────
        names = VGroup(
            self._t("InstructGPT",  size=32, color=TEXT, bold=True),
            self._t("DeepSeek-R1",  size=32, color=TEXT, bold=True),
        ).arrange(RIGHT, buff=1.0)
        box = RoundedRectangle(corner_radius=0.18, width=6.6, height=1.55,
                               fill_opacity=0, stroke_color=TEAL,
                               stroke_width=2.5).move_to(names)
        badge = self._t("MINH BẠCH", size=14, color=TEAL, bold=True)
        badge.next_to(box, UP, buff=-0.05).align_to(box, RIGHT).shift(LEFT*0.2)
        transparent_grp = VGroup(box, names, badge)

        self.play(FadeIn(transparent_grp, scale=0.88,
                         rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(9.3)
        self.play(FadeOut(transparent_grp, rate_func=smooth_step_in_out),
                  run_time=0.9)

        # ── [01:45.6 – 01:56.9] Khát vọng vs Rào cản tính toán ──────────────
        aspiration = self._t("KHÁT VỌNG KHOA HỌC", size=36,
                             color=TEAL, bold=True)
        # Rào cản: thanh nặng rơi từ trên xuống đè lên
        barrier = RoundedRectangle(corner_radius=0.12, width=7.0, height=1.15,
                                   fill_color="#1E293B", fill_opacity=1,
                                   stroke_color=SLATE, stroke_width=2)
        b_lbl   = self._t("RÀO CẢN TÍNH TOÁN", size=28,
                           color=SLATE, bold=True).move_to(barrier)
        barrier_grp = VGroup(barrier, b_lbl).shift(UP*4.2)

        self.play(Write(aspiration, rate_func=smooth_step_in_out), run_time=1.4)
        self.wait(1.8)
        self.play(barrier_grp.animate.move_to(aspiration),
                  rate_func=rush_into,   # ease-in: "rơi xuống"
                  run_time=1.8)
        self.wait(5.4)
        self.play(FadeOut(VGroup(aspiration, barrier_grp),
                          rate_func=smooth_step_in_out), run_time=0.9)

        # ── [01:56.9 – 02:19.6] Học thuật nhỏ bé trước công nghiệp ──────────
        aca_dot  = Circle(radius=0.12, fill_color=BLUE, fill_opacity=1,
                          stroke_color=BLUE).shift(LEFT*3.6)
        aca_lbl  = self._t("Học thuật", size=17, color=BLUE).next_to(
            aca_dot, DOWN, buff=0.18)

        ind_ring = Circle(radius=3.2, fill_color=ROSE, fill_opacity=0.22,
                          stroke_color=ROSE, stroke_width=3).shift(RIGHT*1.2)
        ind_lbl  = self._t("Công nghiệp", size=42, color=ROSE,
                            bold=True).move_to(ind_ring)

        self.play(FadeIn(VGroup(aca_dot, aca_lbl), rate_func=smooth_step_in_out),
                  FadeIn(VGroup(ind_ring, ind_lbl), scale=0.88,
                         rate_func=smooth_step_in_out),
                  run_time=1.5)
        self.wait(10.5)
        self.play(FadeOut(VGroup(aca_dot, aca_lbl),
                          rate_func=smooth_step_in_out), run_time=1.8)
        self.wait(7.1)
        self.play(FadeOut(VGroup(ind_ring, ind_lbl),
                          rate_func=smooth_step_in_out), run_time=1.8)

    # ── helpers ───────────────────────────────────────────────────────────────
    def _industry_block(self):
        rect  = RoundedRectangle(corner_radius=0.18, width=7.0, height=3.5,
                                  fill_color=SURFACE, fill_opacity=0.7,
                                  stroke_color=SLATE, stroke_width=2)
        label = self._t("KHỐI CÔNG NGHIỆP", size=28, color=TEXT, bold=True).next_to(
            rect, UP, buff=0.2)
        # GPU grid: màu ROSE nhạt → không chói
        gpu_sq = VGroup(*[
            Square(side_length=0.21, fill_color=ROSE, fill_opacity=0.75,
                   stroke_width=0.3, stroke_color=BG)
            for _ in range(96)
        ]).arrange_in_grid(8, 12, buff=0.07).move_to(rect)
        return VGroup(rect, label, gpu_sq)

    def _label_panel(self, text, accent):
        rect = RoundedRectangle(corner_radius=0.14, width=4.2, height=2.2,
                                fill_color=SURFACE, fill_opacity=1,
                                stroke_color=accent, stroke_width=2.5)
        lbl  = self._t(text, size=28, color=accent, bold=True,
                       ).move_to(rect)
        return VGroup(rect, lbl)


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 2 — LLM BOOM  (≈ 4.5 phút)
# ═════════════════════════════════════════════════════════════════════════════
class S2_LLMBoom(Scene):
    def _t(self, text, size=26, color=TEXT, bold=False):
        return Text(text, font="Arial", font_size=size, color=color,
                    weight=BOLD if bold else NORMAL)

    def _panel(self, w, h, accent=BLUE):
        return RoundedRectangle(corner_radius=0.14, width=w, height=h,
                                fill_color=SURFACE, fill_opacity=0.95,
                                stroke_color=accent, stroke_width=2.5)

    def construct(self):
        s1_voiceover = [
            ("assets/audio/s1_00_creativity.mp3",          0.0),
            ("assets/audio/s1_01_student_question.mp3",   13.3),
            ("assets/audio/s1_02_own_path.mp3",           26.6),
            ("assets/audio/s1_03_why_irreplaceable.mp3",  41.0),
            ("assets/audio/s1_04_why_it_runs.mp3",        55.7),
            ("assets/audio/s1_05_swe_bench.mp3",          73.9),
            ("assets/audio/s1_06_evaluation_tools.mp3",  113.9),
            ("assets/audio/s1_07_reverse_engineering.mp3",135.6),
            ("assets/audio/s1_08_research_opportunities.mp3",167.4),
            ("assets/audio/s1_09_barrier_compute.mp3",   206.8),
            ("assets/audio/s1_10_barrier_infrastructure.mp3",258.5),
            ("assets/audio/s1_11_barrier_data.mp3",      268.7),
        ]
        for p, t in s1_voiceover:
            self.add_sound(p, time_offset=t)

        # ── [00:00 – 00:13.3] Sáng tạo vs Quy mô ────────────────────────────
        brain_c = Circle(radius=0.78, fill_color=BLUE, fill_opacity=0.82,
                         stroke_color=TEAL, stroke_width=2.5)
        brain_l = self._t("Bộ não\nHọc thuật", size=19, color=TEXT,
                           bold=True).move_to(brain_c)
        brain_grp = VGroup(brain_c, brain_l)
        self.play(FadeIn(brain_grp, scale=0.5,
                         rate_func=smooth_step_in_out), run_time=1.5)

        # 4 thanh rào cản bao quanh — dùng màu nhất quán ROSE
        def _barrier_bar(w, h, pos):
            r = Rectangle(width=w, height=h, fill_color=ROSE,
                           fill_opacity=0.45, stroke_width=0)
            r.move_to(pos)
            return r

        bars = VGroup(
            _barrier_bar(4.2, 0.82, UP*3.15),
            _barrier_bar(4.2, 0.82, DOWN*3.15),
            _barrier_bar(0.82, 4.2, LEFT*5.85),
            _barrier_bar(0.82, 4.2, RIGHT*5.85),
        )
        bar_lbls = VGroup(
            self._t("QUY MÔ",     size=15, color=BG).move_to(bars[0]),
            self._t("TIỀN BẠC",   size=15, color=BG).move_to(bars[1]),
            self._t("TÀI NGUYÊN", size=13, color=BG).move_to(bars[2]).rotate(PI/2),
            self._t("CÔNG NGHỆ",  size=13, color=BG).move_to(bars[3]).rotate(-PI/2),
        )
        industry_cage = VGroup(*[VGroup(b, l) for b, l in zip(bars, bar_lbls)])

        self.play(LaggedStart(*[FadeIn(g, rate_func=smooth_step_in_out)
                                for g in industry_cage], lag_ratio=0.2), run_time=2.0)
        self.wait(0.8)
        # Siết lại → gây áp bức
        self.play(
            industry_cage[0].animate.shift(DOWN*1.25),
            industry_cage[1].animate.shift(UP*1.25),
            industry_cage[2].animate.shift(RIGHT*2.55),
            industry_cage[3].animate.shift(LEFT*2.55),
            rate_func=smooth_step_in_out, run_time=3.5
        )
        self.wait(4.3)
        self.play(FadeOut(industry_cage, rate_func=smooth_step_in_out),
                  FadeOut(brain_grp, rate_func=smooth_step_in_out), run_time=1.2)

        # ── [00:13.3 – 00:26.6] Câu hỏi sinh viên ───────────────────────────
        # Dùng panel thay vì plain text → dễ đọc hơn
        q_panel = self._panel(9.8, 2.0, AMBER)
        q_text  = self._t(
            '"Làm thế nào để nghiên cứu của chúng em\nkhông bị tụt hậu và tạo ra đóng góp thực sự?"',
            size=22, color=AMBER, bold=True
        ).move_to(q_panel)
        q_grp = VGroup(q_panel, q_text).shift(UP*0.8)

        # 5 chấm sinh viên thành hàng gọn
        dots = VGroup(*[
            Circle(radius=0.16, fill_color=BLUE, fill_opacity=0.85,
                   stroke_color=TEAL, stroke_width=1.5)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.3).shift(DOWN*1.6)
        dot_lbls = VGroup(*[
            self._t("SV", size=10, color=SLATE).next_to(d, DOWN, buff=0.06)
            for d in dots
        ])

        self.play(FadeIn(q_grp, shift=UP*0.2, rate_func=smooth_step_in_out),
                  run_time=1.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5,
                                       rate_func=smooth_step_in_out)
                                for d in dots], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(dot_lbls, rate_func=smooth_step_in_out), run_time=0.8)
        self.wait(8.2)
        self.play(FadeOut(VGroup(q_grp, dots, dot_lbls),
                          rate_func=smooth_step_in_out), run_time=1.2)

        # ── [00:26.6 – 00:41.0] Lối đi riêng ────────────────────────────────
        ind_line  = Line(LEFT*5.2, RIGHT*5.2, color=ROSE, stroke_width=3.5).shift(UP*0.9)
        ind_label = self._t("CÔNG NGHIỆP (QUY MÔ)", size=15,
                             color=ROSE).next_to(ind_line, UP, buff=0.15).align_to(ind_line, LEFT)

        # Đường học thuật: rẽ xuống rồi đi ngang → "tìm lối riêng"
        path = VGroup(
            Line(LEFT*5.2 + UP*0.9, LEFT*1.2 + UP*0.9, color=BLUE, stroke_width=4),
            Line(LEFT*1.2 + UP*0.9, LEFT*1.2 + DOWN*1.4, color=BLUE, stroke_width=4),
            Arrow(LEFT*1.2 + DOWN*1.4, RIGHT*5.2 + DOWN*1.4,
                  color=BLUE, stroke_width=4, buff=0),
        )
        aca_label = self._t("HỌC THUẬT (LỐI ĐI RIÊNG)", size=15,
                             color=BLUE).next_to(path[2], DOWN, buff=0.15).align_to(path[2], LEFT)
        math_grp = VGroup(
            self._t("f(x)", size=34, color=AMBER).move_to(LEFT*0.3 + DOWN*0.6),
            self._t("gradient", size=24, color=AMBER).move_to(RIGHT*1.8 + DOWN*1.0),
        )

        self.play(Create(ind_line), Write(ind_label), run_time=1.2)
        self.play(Create(path[0]), run_time=0.7)
        self.play(Create(path[1]), run_time=0.5)
        self.play(GrowArrow(path[2]), Write(aca_label), run_time=1.0)
        self.play(Write(math_grp, rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(7.2)
        self.play(FadeOut(VGroup(ind_line, ind_label, math_grp),
                          rate_func=smooth_step_in_out), run_time=0.8)
        self.play(
            path.animate.scale(1.4).shift(UP*0.8),
            aca_label.animate.shift(UP*0.8),
            rate_func=smooth_step_in_out, run_time=1.2
        )
        self.play(FadeOut(path, aca_label,
                          rate_func=smooth_step_in_out), run_time=0.8)

        # ── [00:41.0 – 00:55.7] Hộp đen công nghiệp ─────────────────────────
        black_box = self._panel(3.2, 3.2, SLATE).shift(RIGHT*2.8)
        black_box.set_fill(color="#000000", opacity=1.0)
        box_lbl   = self._t("HỘP ĐEN\nCÔNG NGHIỆP", size=22,
                             color=SLATE, bold=True).move_to(black_box)

        up_arrow  = Arrow(RIGHT*4.8 + DOWN*1.4, RIGHT*4.8 + UP*1.4,
                          color=ROSE, stroke_width=5.5)
        dollar    = self._t("$", size=50, color=AMBER, bold=True).next_to(
            up_arrow, LEFT, buff=0.15).shift(UP*0.4)

        self.play(FadeIn(VGroup(black_box, box_lbl), shift=RIGHT*0.4,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.play(GrowArrow(up_arrow), run_time=1.0)
        self.play(FadeIn(dollar, rate_func=smooth_step_in_out), run_time=0.6)
        for _ in range(3):
            self.play(dollar.animate.set_opacity(0.15), run_time=0.28)
            self.play(dollar.animate.set_opacity(1.0),  run_time=0.28)
        self.wait(9.92)

        # ── [00:55.7 – 01:13.9] Tại sao nó chạy? ────────────────────────────
        why_lbl = self._t("TẠI SAO NÓ CHẠY?", size=26,
                           color=TEAL, bold=True).shift(LEFT*3.2 + UP*1.4)
        # Vòng nét đứt + giọt tri thức
        dashed_base = Circle(radius=1.0, color=BLUE, stroke_width=2.5,
                             stroke_opacity=0.8).shift(LEFT*3.2 + DOWN*0.9)
        dashed_c    = DashedVMobject(dashed_base, num_dashes=20)
        drop_shape  = Ellipse(width=0.7, height=1.0,
                              fill_color=TEAL, fill_opacity=0.88,
                              stroke_width=1, stroke_color=TEAL).move_to(dashed_base)
        drop_lbl    = self._t("Tri thức\ngốc rễ", size=14,
                               color=TEXT, bold=True).move_to(drop_shape)
        left_grp    = VGroup(why_lbl, dashed_c, drop_shape, drop_lbl)

        self.play(Write(why_lbl, rate_func=smooth_step_in_out), run_time=1.5)
        self.play(Create(dashed_c), run_time=1.2)
        self.play(FadeIn(drop_shape, scale=0.5,
                         rate_func=smooth_step_in_out),
                  Write(drop_lbl, rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(12.8)
        self.play(FadeOut(VGroup(left_grp, black_box, box_lbl,
                                 up_arrow, dollar),
                          rate_func=smooth_step_in_out), run_time=1.5)

        # ── [01:13.9 – 01:53.9] SWE-bench ───────────────────────────────────
        swe_panel = self._panel(5.0, 1.5, BLUE)
        swe_title = self._t("SWE-bench  (ICLR 2024)", size=26,
                             color=BLUE, bold=True).move_to(swe_panel)
        swe_grp   = VGroup(swe_panel, swe_title)

        # Check / Cross → dùng cùng kích thước, căn giữa
        def _verdict(sym_tex, text, color, side):
            sym = self._t(sym_tex, size=30, color=color, bold=True)
            txt = self._t(text, size=22, color=color, bold=True)
            return VGroup(sym, txt).arrange(RIGHT, buff=0.15).shift(side * 2.4 + DOWN*1.5)

        check_grp = _verdict("[OK]", "Có thể làm",    TEAL, LEFT)
        cross_grp = _verdict("[X]",  "Không thể làm", ROSE, RIGHT)

        self.play(FadeIn(swe_grp, scale=0.82,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(9.5)
        self.play(FadeIn(check_grp, shift=UP*0.18,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.play(FadeIn(cross_grp, shift=UP*0.18,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(25.5)
        self.play(
            swe_grp.animate.scale(0.52).to_corner(UL, buff=0.4),
            FadeOut(VGroup(check_grp, cross_grp),
                    rate_func=smooth_step_in_out),
            run_time=1.5
        )

        # ── [01:53.9 – 02:15.6] Evaluation tools ────────────────────────────
        eval_data = [
            ("CharXiv  (Biểu đồ)",      TEAL),
            ("SorryBench  (An toàn)",    BLUE),
            ("HELMET  (Ngữ cảnh dài)",  AMBER),
        ]
        eval_cards = VGroup()
        for i, (txt, col) in enumerate(eval_data):
            p = self._panel(5.0, 0.82, col)
            l = self._t(txt, size=20, color=col, bold=True).move_to(p)
            eval_cards.add(VGroup(p, l).shift(DOWN*(i*1.05 - 0.5)))

        for card in eval_cards:
            self.play(FadeIn(card, scale=0.88,
                             rate_func=smooth_step_in_out), run_time=1.0)
            self.wait(3.5)
        self.wait(6.7)
        self.play(eval_cards.animate.scale(0.5).to_corner(UR, buff=0.4),
                  rate_func=smooth_step_in_out, run_time=1.5)

        # ── [02:15.6 – 02:47.4] Reverse Engineer ────────────────────────────
        self.play(FadeOut(swe_grp, eval_cards,
                          rate_func=smooth_step_in_out), run_time=0.9)

        rev_lbl = self._t("REVERSE ENGINEER", size=30,
                           color=TEAL, bold=True).shift(UP*1.1)

        # 3 node + 2 connector → mô phỏng mạch nhỏ
        nodes = VGroup(*[
            Circle(radius=0.28, fill_color=TEAL, fill_opacity=0.8,
                   stroke_color=TEAL)
            .shift(LEFT*(2.8 - i*1.4) + DOWN*0.9)
            for i in range(3)
        ])
        connectors = VGroup(*[
            Line(nodes[i].get_right(), nodes[i+1].get_left(),
                 color=TEAL, stroke_width=2)
            for i in range(2)
        ])
        rev_arrow = Arrow(RIGHT*4.6 + DOWN*0.9, LEFT*3.6 + DOWN*0.9,
                          color=ROSE, stroke_width=5, buff=0)

        self.play(Write(rev_lbl, rate_func=smooth_step_in_out), run_time=1.5)
        self.play(FadeIn(nodes, rate_func=smooth_step_in_out),
                  Create(connectors), run_time=1.2)
        self.play(GrowArrow(rev_arrow), run_time=1.5)
        self.wait(25.2)
        self.play(FadeOut(VGroup(rev_lbl, nodes, connectors, rev_arrow),
                          rate_func=smooth_step_in_out), run_time=1.5)

        # ── [02:47.4 – 03:26.9] 3 hướng nghiên cứu → 3 rào cản ─────────────
        opps = VGroup(
            self._t("1. Tác nhân (Agents)",      size=25, color=TEAL,  bold=True),
            self._t("2. Lý thuyết & Suy luận",   size=25, color=BLUE,  bold=True),
            self._t("3. Chính sách an toàn",      size=25, color=AMBER, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).shift(LEFT*1.8 + UP*0.4)

        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT*0.25,
                                       rate_func=smooth_step_in_out)
                                for b in opps], lag_ratio=0.45), run_time=2.5)
        self.wait(34.9)

        # 3 thanh rào cản — màu nhất quán SLATE
        barriers = VGroup(*[
            RoundedRectangle(corner_radius=0.1, width=9.0, height=0.92,
                             fill_color=SURFACE, fill_opacity=1,
                             stroke_color=SLATE, stroke_width=1.5)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.42).move_to(ORIGIN)

        self.play(FadeOut(opps, rate_func=smooth_step_in_out),
                  LaggedStart(*[FadeIn(b, scale=0.85,
                                       rate_func=smooth_step_in_out)
                                for b in barriers], lag_ratio=0.2),
                  run_time=2.0)
        self.wait(9.0)

        # ── [03:26.9 – 04:18.6] Rào cản 1 — Compute ─────────────────────────
        # Keep every label attached to its barrier and above the filled shapes.
        c_lbl = self._t("1. COMPUTE", size=19, color=TEXT,
                        bold=True).move_to(barriers[0])
        i_lbl = self._t("2. INFRASTRUCTURE", size=15, color=TEXT,
                        bold=True).move_to(barriers[1])
        d_lbl = self._t("3. PROPRIETARY DATA", size=13, color=TEXT,
                        bold=True).move_to(barriers[2])
        b_lbls = VGroup(c_lbl, i_lbl, d_lbl)

        barriers.set_z_index(5)
        b_lbls.set_z_index(20)
        i_lbl.set_opacity(0)
        d_lbl.set_opacity(0)
        barrier_stack = VGroup(barriers, b_lbls)

        self.play(Write(c_lbl, rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(9.0)
        self.play(
            barrier_stack.animate.scale(0.78).shift(LEFT*3.2),
            rate_func=smooth_step_in_out, run_time=1.5
        )

        # Biểu đồ tương phản — dot nhỏ / vòng lớn
        micro = Circle(radius=0.1, fill_color=BLUE, fill_opacity=1,
                       stroke_width=0.5, stroke_color=TEAL).shift(RIGHT*1.8+DOWN*0.6)
        micro_lbl = self._t("Học thuật\n0.001%", size=12,
                             color=BLUE).next_to(micro, DOWN, buff=0.08)
        giant = Circle(radius=2.0, fill_color=ROSE, fill_opacity=0.2,
                       stroke_color=ROSE, stroke_width=3).shift(RIGHT*3.6+UP*0.4)
        giant_lbl = self._t("Công nghiệp\n100%", size=19,
                             color=ROSE, bold=True).move_to(giant)
        contrast = VGroup(micro, micro_lbl, giant, giant_lbl)

        self.play(FadeIn(contrast, scale=0.7,
                         rate_func=smooth_step_in_out), run_time=2.0)
        self.wait(27.8)
        self.play(FadeOut(contrast, rate_func=smooth_step_in_out), run_time=1.2)

        # ── [04:18.6 – 04:28.8] Rào cản 2 — Infrastructure ──────────────────
        self.play(i_lbl.animate.set_opacity(1),
                  rate_func=smooth_step_in_out, run_time=0.9)

        gpu_box = self._panel(1.8, 0.75, TEAL).shift(RIGHT*2.4 + DOWN*0.5)
        gpu_lbl = self._t("1× GPU", size=15, color=TEAL,
                           bold=True).move_to(gpu_box)
        time_txt = self._t("02:00 AM", size=23, color=AMBER,
                            bold=True).shift(RIGHT*2.4 + UP*0.4)

        self.play(FadeIn(VGroup(gpu_box, gpu_lbl), rate_func=smooth_step_in_out),
                  FadeIn(time_txt, rate_func=smooth_step_in_out), run_time=1.0)
        for _ in range(2):
            self.play(time_txt.animate.set_opacity(0.15), run_time=0.28)
            self.play(time_txt.animate.set_opacity(1.0),  run_time=0.28)
        self.wait(6.38)
        self.play(FadeOut(VGroup(gpu_box, gpu_lbl, time_txt),
                          rate_func=smooth_step_in_out), run_time=0.8)

        # ── [04:28.8 – 04:46.7] Rào cản 3 — Proprietary Data ────────────────
        self.play(d_lbl.animate.set_opacity(1),
                  rate_func=smooth_step_in_out, run_time=1.2)
        self.wait(3.8)

        # Mũi tên "vượt qua" mỗi rào cản
        out_arrows = VGroup(*[
            Arrow(b.get_right() + RIGHT*0.15, b.get_right() + RIGHT*1.3,
                  color=TEAL, stroke_width=3.5)
            for b in barriers
        ])
        self.play(
            barriers[0].animate.set_stroke(color=BLUE),
            barriers[1].animate.set_stroke(color=BLUE),
            barriers[2].animate.set_stroke(color=BLUE),
            LaggedStart(*[GrowArrow(a) for a in out_arrows], lag_ratio=0.22),
            run_time=2.0
        )
        self.wait(9.4)
        self.play(
            FadeOut(VGroup(barrier_stack, out_arrows),
                    rate_func=smooth_step_in_out),
            run_time=1.5
        )


# ═════════════════════════════════════════════════════════════════════════════
# SCENE 3 — WHY ACADEMIA STILL MATTERS  (≈ 5 phút)
# ═════════════════════════════════════════════════════════════════════════════
class S3_WhyMatters(Scene):
    def _t(self, text, size=26, color=TEXT, bold=False):
        return Text(text, font="Arial", font_size=size, color=color,
                    weight=BOLD if bold else NORMAL)

    def _panel(self, w, h, accent=BLUE):
        return RoundedRectangle(corner_radius=0.14, width=w, height=h,
                                fill_color=SURFACE, fill_opacity=0.95,
                                stroke_color=accent, stroke_width=2.5)

    def construct(self):
        s3_voiceover = [
            ("assets/audio/s3_00_slms_pillar.mp3",          0.0),
            ("assets/audio/s3_01_why_slms.mp3",            10.1),
            ("assets/audio/s3_02_no_budget.mp3",           15.1),
            ("assets/audio/s3_03_easy_to_run.mp3",         19.6),
            ("assets/audio/s3_04_downloads_llama.mp3",     28.3),
            ("assets/audio/s3_05_llama1_gpt3.mp3",         40.9),
            ("assets/audio/s3_06_ask_academic.mp3",        51.3),
            ("assets/audio/s3_07_gpu_hours_cost.mp3",      58.2),
            ("assets/audio/s3_08_be_smarter.mp3",          68.9),
            ("assets/audio/s3_09_sheared_llama_princeton.mp3",77.4),
            ("assets/audio/s3_10_how_it_works.mp3",        81.6),
            ("assets/audio/s3_11_two_steps.mp3",           93.6),
            ("assets/audio/s3_12_step_one_pruning.mp3",    96.0),
            ("assets/audio/s3_13_pruning_details.mp3",    105.5),
            ("assets/audio/s3_14_constrained_optimization.mp3",117.5),
            ("assets/audio/s3_15_lagrange.mp3",           121.8),
            ("assets/audio/s3_16_resources_split.mp3",    130.5),
            ("assets/audio/s3_17_what_data.mp3",          143.6),
            ("assets/audio/s3_18_red_pyjama.mp3",         148.7),
            ("assets/audio/s3_19_random_data.mp3",        159.1),
            ("assets/audio/s3_20_failure.mp3",            163.3),
            ("assets/audio/s3_21_loss_imbalance.mp3",     165.7),
            ("assets/audio/s3_22_c4_vs_github.mp3",       174.3),
            ("assets/audio/s3_23_scaling_laws.mp3",       183.7),
            ("assets/audio/s3_24_predict_reference_loss.mp3",192.3),
            ("assets/audio/s3_25_optimal_mixtures.mp3",   200.9),
            ("assets/audio/s3_26_gained_fruits.mp3",      211.3),
            ("assets/audio/s3_27_cheap_resource.mp3",     222.2),
            ("assets/audio/s3_28_sota.mp3",               236.1),
            ("assets/audio/s3_29_downloads_hf.mp3",       247.3),
            ("assets/audio/s3_30_industry_adopted.mp3",   256.0),
            ("assets/audio/s3_31_qwen_limit.mp3",         273.8),
        ]
        for p, t in s3_voiceover:
            self.add_sound(p, time_offset=t)

        # ── [00:00 – 00:10.1] Trụ cột 1: SLMs ───────────────────────────────
        section_badge = self._panel(8.2, 0.7, TEAL)
        section_badge.to_edge(UP, buff=0.3)
        section_lbl = self._t("TRỤ CỘT 1 : SMALL LANGUAGE MODELS",
                               size=22, color=TEAL, bold=True).move_to(section_badge)
        slm_c  = Circle(radius=0.72, fill_color=BLUE, fill_opacity=0.82,
                        stroke_color=TEAL, stroke_width=2.5)
        slm_l  = self._t("SLMs\n(1B – 10B)", size=17,
                          color=TEXT, bold=True).move_to(slm_c)
        slm_grp = VGroup(slm_c, slm_l)

        self.play(FadeIn(VGroup(section_badge, section_lbl),
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.play(FadeIn(slm_grp, scale=0.5,
                         rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(0.9)
        self.play(slm_grp.animate.shift(UP*1.4),
                  rate_func=smooth_step_in_out, run_time=1.2)
        self.wait(5.8)

        # ── [00:10.1 – 00:15.1] Tại sao SLMs bùng nổ? ───────────────────────
        q_mark = self._t("?", size=62, color=AMBER, bold=True).next_to(slm_c, RIGHT, buff=0.4)
        self.play(FadeIn(q_mark, scale=0.3,
                         rate_func=smooth_step_in_out), run_time=0.8)
        self.wait(3.5)
        self.play(FadeOut(q_mark, rate_func=smooth_step_in_out), run_time=0.8)

        # ── [00:15.1 – 00:19.6] Ngân sách học thuật giới hạn ─────────────────
        no_budget = self._panel(7.8, 0.85, ROSE)
        no_budget_lbl = self._t("[X]  Ngân sách học thuật để chạy đua mô hình lớn",
                                 size=19, color=ROSE, bold=True).move_to(no_budget)
        no_budget_grp = VGroup(no_budget, no_budget_lbl).shift(DOWN*0.4)
        self.play(FadeIn(no_budget_grp, shift=UP*0.15,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(no_budget_grp, rate_func=smooth_step_in_out), run_time=1.0)

        # ── [00:19.6 – 00:28.3] Tính linh hoạt của SLMs ─────────────────────
        feats = VGroup(
            self._t("+ Dễ chạy",       size=17, color=TEXT),
            self._t("+ Dễ tinh chỉnh", size=17, color=TEXT),
            self._t("+ Thiết bị biên", size=17, color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).shift(DOWN*0.45)
        feat_box = self._panel(3.2, 1.75, BLUE).move_to(feats)

        self.play(FadeIn(feat_box, rate_func=smooth_step_in_out), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT*0.15,
                                       rate_func=smooth_step_in_out)
                                for f in feats], lag_ratio=0.25), run_time=1.5)
        self.wait(4.9)
        self.play(FadeOut(VGroup(section_badge, section_lbl, slm_grp,
                                  feat_box, feats),
                          rate_func=smooth_step_in_out), run_time=1.5)

        # ── [00:28.3 – 00:40.9] Biểu đồ lượt tải Llama 3 ────────────────────
        chart_lbl = self._t("LƯỢT TẢI XUỐNG LLAMA 3 (TƯƠNG ĐỐI)",
                             size=20, color=TEAL, bold=True).to_edge(UP, buff=0.4)
        base_y = DOWN * 2.2
        # Dùng cùng màu BLUE, chiều cao khác → dễ so sánh
        def _bar(w, h, col, xpos, label, val_txt):
            b   = Rectangle(width=w, height=h, fill_color=col,
                             fill_opacity=0.85, stroke_color=col, stroke_width=1.5)
            b.move_to(base_y + RIGHT*xpos + UP*(h/2))
            lbl = self._t(label,   size=17, color=TEXT).next_to(b, DOWN, buff=0.12)
            val = self._t(val_txt, size=13, color=col).next_to(b, UP,   buff=0.08)
            return VGroup(b, lbl, val)

        bar_3b  = _bar(0.85, 3.4, BLUE,  -2.0, "3B",  "Rất cao")
        bar_8b  = _bar(0.85, 4.1, TEAL,   0.0, "8B",  "Vượt trội")
        bar_70b = _bar(0.85, 0.6, ROSE,   2.0, "70B", "Thấp")
        chart_grp = VGroup(chart_lbl, bar_3b, bar_8b, bar_70b)

        self.play(FadeIn(chart_lbl, rate_func=smooth_step_in_out), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(g, shift=UP*0.2,
                                       rate_func=smooth_step_in_out)
                                for g in [bar_3b, bar_8b, bar_70b]], lag_ratio=0.3),
                  run_time=1.8)
        self.wait(8.5)
        self.play(chart_grp.animate.scale(0.62).to_edge(LEFT, buff=0.5),
                  rate_func=smooth_step_in_out, run_time=1.5)

        # ── [00:40.9 – 00:51.3] Llama 13B đẩy lùi GPT-3 ────────────────────
        llama_lbl  = self._t("Llama-1  13B",   size=21, color=BLUE,  bold=True).shift(RIGHT*0.5 + UP*0.4)
        vs_lbl     = self._t("VS",              size=17, color=SLATE).shift(RIGHT*2.1 + UP*0.4)
        gpt_lbl    = self._t("GPT-3  175B",     size=20, color=ROSE,  bold=True).shift(RIGHT*4.2 + UP*0.4)

        self.play(FadeIn(VGroup(llama_lbl, vs_lbl, gpt_lbl),
                         rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(1.8)
        push_arr = Arrow(llama_lbl.get_right(), gpt_lbl.get_left(),
                         color=TEAL, stroke_width=3.5, buff=0.12)
        self.play(GrowArrow(push_arr), run_time=0.8)
        self.play(
            gpt_lbl.animate.shift(RIGHT*4.0).set_opacity(0),
            llama_lbl.animate.move_to(RIGHT*2.4 + UP*0.4),
            FadeOut(VGroup(vs_lbl, push_arr), rate_func=smooth_step_in_out),
            rate_func=smooth_step_in_out, run_time=1.2
        )
        self.wait(4.2)
        self.play(FadeOut(VGroup(chart_grp, llama_lbl, gpt_lbl),
                          rate_func=smooth_step_in_out), run_time=1.2)

        # ── [00:51.3 – 00:58.2] Câu hỏi tự tạo mô hình ──────────────────────
        q2 = self._panel(8.2, 1.1, AMBER)
        q2_lbl = self._t("Giới học thuật tự tạo mô hình 1B / 3B?",
                          size=23, color=AMBER, bold=True).move_to(q2)
        self.play(FadeIn(VGroup(q2, q2_lbl), shift=UP*0.15,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(4.6)

        # ── [00:58.2 – 01:08.9] Chi phí huấn luyện ──────────────────────────
        cost_p = self._panel(8.6, 1.1, SLATE)
        cost_l = self._t("Huấn luyện 3B từ đầu (1 Nghìn tỷ Tokens)  =",
                          size=19, color=TEXT).move_to(cost_p)
        cost_grp = VGroup(cost_p, cost_l).shift(UP*0.9)

        gpu_p = self._panel(5.0, 1.1, ROSE)
        gpu_p.set_fill(color=SURFACE)
        gpu_l = self._t("30.000 GIỜ GPU", size=34, color=ROSE, bold=True).move_to(gpu_p)
        gpu_grp = VGroup(gpu_p, gpu_l).shift(DOWN*0.4)

        self.play(FadeOut(VGroup(q2, q2_lbl), rate_func=smooth_step_in_out),
                  run_time=0.8)
        self.play(FadeIn(cost_grp, shift=UP*0.15,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.play(FadeIn(gpu_grp, scale=0.55,
                         rate_func=smooth_step_in_out), run_time=1.0)
        for _ in range(3):
            self.play(gpu_l.animate.set_opacity(0.18), run_time=0.32)
            self.play(gpu_l.animate.set_opacity(1.0),  run_time=0.32)
        self.wait(6.78)

        # ── [01:08.9 – 01:17.4] Phải thông minh hơn ─────────────────────────
        cross_p = self._panel(7.2, 0.78, ROSE)
        cross_l = self._t("[X]  Vượt xa nguồn lực học thuật",
                           size=17, color=ROSE, bold=True).move_to(cross_p)
        cross_grp = VGroup(cross_p, cross_l).next_to(gpu_grp, DOWN, buff=0.4)

        smarter_p = self._panel(7.2, 1.1, BLUE)
        smarter_l = self._t("BẮT BUỘC PHẢI THÔNG MINH HƠN",
                             size=27, color=BLUE, bold=True).move_to(smarter_p)
        smarter_grp = VGroup(smarter_p, smarter_l)

        self.play(FadeIn(cross_grp, rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(VGroup(cost_grp, gpu_grp, cross_grp),
                          rate_func=smooth_step_in_out), run_time=1.0)
        self.play(FadeIn(smarter_grp, scale=0.82,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(smarter_grp, rate_func=smooth_step_in_out), run_time=1.0)

        # ── [01:17.4 – 01:21.6] Dự án Sheared LLaMA ─────────────────────────
        proj_hdr = self._panel(8.4, 0.72, TEAL)
        proj_hdr.to_edge(UP, buff=0.3)
        proj_lbl = self._t("DỰ ÁN : SHEARED LLAMA  (Princeton)",
                            size=22, color=TEAL, bold=True).move_to(proj_hdr)
        self.play(FadeIn(VGroup(proj_hdr, proj_lbl),
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(3.2)

        # ── [01:21.6 – 01:33.6] Gọt giũa mô hình lớn ────────────────────────
        src_sq  = Square(side_length=1.9, fill_color=ROSE, fill_opacity=0.35,
                         stroke_color=ROSE, stroke_width=2.5).shift(LEFT*3.0 + DOWN*0.5)
        src_lbl = self._t("Llama 7B", size=17, color=TEXT, bold=True).move_to(src_sq)
        src_grp = VGroup(src_sq, src_lbl)

        tgt_sq  = Square(side_length=0.88, fill_color=BLUE, fill_opacity=0.65,
                         stroke_color=TEAL, stroke_width=2.0).shift(RIGHT*3.0 + DOWN*0.5)
        tgt_lbl = self._t("3B", size=14, color=TEXT, bold=True).move_to(tgt_sq)
        tgt_grp = VGroup(tgt_sq, tgt_lbl)

        shear_arr = Arrow(src_sq.get_right(), tgt_sq.get_left(),
                          color=AMBER, stroke_width=4, buff=0.05)
        shear_lbl = self._t("Gọt giũa", size=15, color=AMBER).next_to(shear_arr, UP, buff=0.12)

        self.play(FadeIn(src_grp, scale=0.72,
                         rate_func=smooth_step_in_out), run_time=1.2)
        self.play(GrowArrow(shear_arr),
                  FadeIn(shear_lbl, rate_func=smooth_step_in_out), run_time=1.0)
        self.play(FadeIn(tgt_grp, scale=0.72,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(6.8)
        self.play(
            FadeOut(VGroup(tgt_grp, shear_arr, shear_lbl),
                    rate_func=smooth_step_in_out),
            src_grp.animate.move_to(LEFT*2.8 + DOWN*0.5).scale(1.08),
            rate_func=smooth_step_in_out, run_time=2.0
        )

        # ── [01:33.6 – 01:36.0] Quy trình 2 bước ────────────────────────────
        steps_lbl = self._t("QUY TRÌNH 2 BƯỚC", size=21,
                             color=AMBER, bold=True).shift(RIGHT*2.4 + UP*0.5)
        self.play(Write(steps_lbl, rate_func=smooth_step_in_out), run_time=0.9)
        self.wait(1.5)

        # ── [01:36.0 – 01:45.5] Structural Pruning ───────────────────────────
        dashed_base = Square(side_length=2.4, color=BLUE, stroke_width=2.0).move_to(src_sq)
        dashed_sq   = DashedVMobject(dashed_base, num_dashes=20)
        subnet_lbl  = self._t("Mạng con (Subnetwork)", size=12,
                               color=BLUE).next_to(dashed_base, UP, buff=0.08)
        pruning_lbl = self._t("Structural Pruning", size=17,
                               color=TEAL, bold=True).shift(RIGHT*2.4 + DOWN*0.8)

        self.play(FadeOut(steps_lbl, rate_func=smooth_step_in_out), run_time=0.5)
        self.play(Create(dashed_sq), Write(subnet_lbl), run_time=1.5)
        self.play(Write(pruning_lbl, rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(6.0)

        # ── [01:45.5 – 01:57.5] Chi tiết cắt tỉa ────────────────────────────
        att_p = self._panel(1.9, 0.6, SLATE).shift(LEFT*2.5 + UP*0.4)
        att_l = self._t("Attention Heads", size=11, color=SLATE).move_to(att_p)
        dim_p = self._panel(1.9, 0.6, SLATE).shift(LEFT*2.5 + DOWN*1.4)
        dim_l = self._t("Chiều trung gian", size=11, color=SLATE).move_to(dim_p)

        self.play(FadeIn(VGroup(att_p, att_l)),
                  FadeIn(VGroup(dim_p, dim_l)),
                  rate_func=smooth_step_in_out, run_time=1.0)
        # Thanh quét → bị xóa
        sweep = Line(UP*2.0 + LEFT*4.2, DOWN*3.0 + LEFT*4.2,
                     color=ROSE, stroke_width=3.5)
        self.play(FadeIn(sweep, rate_func=smooth_step_in_out), run_time=0.4)
        self.play(
            sweep.animate.shift(RIGHT*3.2),
            VGroup(att_p, att_l).animate.shift(RIGHT*3.2).set_opacity(0),
            VGroup(dim_p, dim_l).animate.shift(RIGHT*3.2).set_opacity(0),
            rate_func=smooth_step_in_out, run_time=1.8
        )
        self.play(FadeOut(VGroup(sweep, dashed_sq, subnet_lbl,
                                  pruning_lbl, src_grp, att_p, att_l,
                                  dim_p, dim_l),
                          rate_func=smooth_step_in_out), run_time=0.8)

        arch_p = self._panel(8.0, 1.2, TEAL)
        arch_l = self._t("Kiến trúc mục tiêu :  32 Lớp  |  20 Đầu  |  Chiều ẩn 2560",
                          size=19, color=TEAL, bold=True).move_to(arch_p)
        arch_grp = VGroup(arch_p, arch_l)
        self.play(FadeIn(arch_grp, scale=0.88,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(6.4)

        # ── [01:57.5 – 02:01.8] Tối ưu ràng buộc ────────────────────────────
        box_c = RoundedRectangle(corner_radius=0.15, width=6.4, height=1.7,
                                  fill_opacity=0, stroke_color=SLATE,
                                  stroke_width=2.0).move_to(arch_grp)
        c_lbl2 = self._t("Tối ưu hóa có ràng buộc", size=15,
                           color=AMBER).next_to(box_c, UP, buff=0.12)
        self.play(Create(box_c), Write(c_lbl2,
                                       rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(3.2)

        # ── [02:01.8 – 02:10.5] Lagrange ─────────────────────────────────────
        lag_formula = self._t(
            "L(x, lambda) = f(x) + lambda * g(x)",
            size=20, color=AMBER
        ).shift(RIGHT*3.8 + UP*1.9)
        self.play(Write(lag_formula, rate_func=smooth_step_in_out), run_time=1.2)

        fit_sq  = Square(side_length=1.75, fill_color=BLUE,
                          fill_opacity=0.82, stroke_color=TEAL,
                          stroke_width=2.5).move_to(ORIGIN)
        fit_lbl = self._t("Kiến trúc\nvừa vặn", size=17,
                           color=TEXT, bold=True).move_to(fit_sq)
        fit_grp = VGroup(fit_sq, fit_lbl)

        self.play(
            Transform(box_c, fit_sq),
            Transform(arch_grp, fit_lbl),
            FadeOut(c_lbl2, rate_func=smooth_step_in_out),
            run_time=2.0
        )
        self.wait(5.4)

        # ── [02:10.5 – 02:23.7] Tỷ lệ phân bổ tài nguyên ────────────────────
        self.play(
            FadeOut(lag_formula, rate_func=smooth_step_in_out),
            box_c.animate.scale(0.82).shift(LEFT*3.6),
            arch_grp.animate.scale(0.82).shift(LEFT*3.6),
            rate_func=smooth_step_in_out, run_time=1.2
        )

        bar_bg = Rectangle(width=6.0, height=0.42, fill_color=SURFACE,
                           fill_opacity=0.6, stroke_color=SLATE,
                           stroke_width=1.5).shift(RIGHT*2.2 + DOWN*0.5)
        bar_1  = Rectangle(width=0.06, height=0.42, fill_color=ROSE,
                            fill_opacity=0.95, stroke_width=0)\
                    .next_to(bar_bg.get_left(), RIGHT, buff=0)
        lbl_1  = self._t("1% Cắt tỉa", size=12, color=ROSE)\
                    .next_to(bar_1, UP, buff=0.12)
        bar_99 = Rectangle(width=5.94, height=0.42, fill_color=BLUE,
                            fill_opacity=0.85, stroke_width=0)\
                    .next_to(bar_1, RIGHT, buff=0)
        lbl_99 = self._t("99% Huấn luyện tiếp tục  (Hồi phục tri thức)",
                          size=12, color=BLUE).next_to(bar_99, DOWN, buff=0.12)

        self.play(Create(bar_bg), run_time=0.8)
        self.play(FadeIn(bar_1), Write(lbl_1,
                                       rate_func=smooth_step_in_out), run_time=0.8)
        self.play(FadeIn(bar_99), Write(lbl_99,
                                        rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(7.9)
        self.play(FadeOut(VGroup(bar_bg, bar_1, lbl_1, bar_99, lbl_99,
                                  box_c, arch_grp, proj_hdr, proj_lbl),
                          rate_func=smooth_step_in_out), run_time=1.5)

        # ── [02:23.7 – 02:28.7] Dữ liệu hồi phục ────────────────────────────
        q3_p  = self._panel(9.2, 1.1, AMBER)
        q3_l  = self._t("Mô hình sẽ ăn dữ liệu gì để hồi phục tri thức?",
                         size=22, color=AMBER, bold=True).move_to(q3_p)
        self.play(FadeIn(VGroup(q3_p, q3_l), shift=UP*0.15,
                         rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(2.8)
        self.play(FadeOut(VGroup(q3_p, q3_l),
                          rate_func=smooth_step_in_out), run_time=1.0)

        # ── [02:28.7 – 02:39.1] Red Pyjama dataset ───────────────────────────
        hub_c  = Circle(radius=0.88, fill_color=ROSE, fill_opacity=0.65,
                         stroke_color=ROSE, stroke_width=2.0).shift(LEFT*3.0)
        hub_l  = self._t("Red\nPyjama", size=17, color=TEXT, bold=True).move_to(hub_c)
        hub_grp = VGroup(hub_c, hub_l)

        node_data = ["Common Crawl", "GitHub", "Sách & Bài báo KH"]
        node_grps = VGroup()
        arrows_grp = VGroup()
        for i, nd in enumerate(node_data):
            p = self._panel(3.1, 0.58, TEAL).shift(RIGHT*2.6 + UP*(1.2 - i*1.2))
            l = self._t(nd, size=13, color=TEAL).move_to(p)
            node_grps.add(VGroup(p, l))
            arr = Arrow(hub_c.get_right(), p.get_left(),
                        color=SLATE, stroke_width=2.0)
            arrows_grp.add(arr)
        data_grp = VGroup(hub_grp, node_grps, arrows_grp)

        self.play(FadeIn(hub_grp, scale=0.72,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_grp], lag_ratio=0.2),
                  run_time=1.2)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT*0.2,
                                       rate_func=smooth_step_in_out)
                                for n in node_grps], lag_ratio=0.2), run_time=1.2)
        self.wait(5.0)
        self.play(data_grp.animate.scale(0.5).to_corner(UL, buff=0.3),
                  rate_func=smooth_step_in_out, run_time=2.0)

        # ── [02:39.1 – 02:43.3] Bốc ngẫu nhiên? ─────────────────────────────
        q_rand_p = self._panel(6.2, 0.95, AMBER)
        q_rand_l = self._t("Bốc ngẫu nhiên dữ liệu  = ?",
                            size=23, color=AMBER, bold=True).move_to(q_rand_p)
        q_rand_p.shift(RIGHT*1.5 + DOWN*0.4)
        q_rand_l.move_to(q_rand_p)
        self.play(FadeIn(VGroup(q_rand_p, q_rand_l), shift=UP*0.12,
                         rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(3.0)

        # ── [02:43.3 – 02:45.7] Thất bại ────────────────────────────────────
        fail_p = self._panel(4.0, 1.1, ROSE)
        fail_p.set_fill(color="#2D0A0A")
        fail_l = self._t("THẤT BẠI", size=40, color=ROSE, bold=True).move_to(fail_p)
        fail_grp = VGroup(fail_p, fail_l).move_to(q_rand_p)

        self.play(
            FadeOut(VGroup(q_rand_p, q_rand_l), rate_func=smooth_step_in_out),
            FadeIn(fail_grp, scale=0.78, rate_func=smooth_step_in_out),
            run_time=0.55
        )
        for _ in range(2):
            self.play(fail_l.animate.set_opacity(0.15), run_time=0.18)
            self.play(fail_l.animate.set_opacity(1.0),  run_time=0.18)
        self.wait(0.53)
        self.play(FadeOut(VGroup(fail_grp, data_grp),
                          rate_func=smooth_step_in_out), run_time=0.6)

        # ── [02:45.7 – 02:54.3] Mất cân bằng Loss ────────────────────────────
        loss_hdr = self._panel(8.0, 0.7, AMBER).to_edge(UP, buff=0.3)
        loss_hdr_l = self._t("NGHỊCH LÝ : MẤT CÂN BẰNG LOSS",
                              size=21, color=AMBER, bold=True).move_to(loss_hdr)
        base_ln = Line(LEFT*4.5 + DOWN*2.0, RIGHT*4.5 + DOWN*2.0,
                       color=SLATE, stroke_width=2)
        self.play(FadeIn(VGroup(loss_hdr, loss_hdr_l),
                         rate_func=smooth_step_in_out),
                  Create(base_ln), run_time=1.5)
        self.wait(7.1)

        # ── [02:54.3 – 03:03.7] C4 vs Github ────────────────────────────────
        bar_c4 = Rectangle(width=1.0, height=3.4, fill_color=ROSE,
                           fill_opacity=0.82, stroke_color=ROSE,
                           stroke_width=1.5).shift(LEFT*1.5 + DOWN*0.3)
        lbl_c4 = self._t("C4  (Loss cao)", size=13,
                          color=ROSE).next_to(bar_c4, DOWN, buff=0.12)

        bar_gh = Rectangle(width=1.0, height=0.88, fill_color=BLUE,
                            fill_opacity=0.82, stroke_color=BLUE,
                            stroke_width=1.5).shift(RIGHT*1.5 + DOWN*1.56)
        lbl_gh = self._t("GitHub  (Loss thấp)", size=13,
                          color=BLUE).next_to(bar_gh, DOWN, buff=0.12)

        warn_p = self._panel(7.2, 0.75, ROSE)
        warn_l = self._t("MÔ HÌNH BỊ LỆCH LẠC KIẾN THỨC",
                          size=18, color=ROSE, bold=True).move_to(warn_p)
        warn_grp = VGroup(warn_p, warn_l).shift(UP*0.75)

        self.play(FadeIn(VGroup(bar_c4, lbl_c4), shift=UP*0.2),
                  FadeIn(VGroup(bar_gh, lbl_gh), shift=UP*0.2),
                  rate_func=smooth_step_in_out, run_time=1.5)
        self.play(FadeIn(warn_grp, scale=0.88,
                         rate_func=smooth_step_in_out), run_time=1.0)
        self.wait(6.9)

        # ── [03:03.7 – 03:12.4] Scaling Laws can thiệp ───────────────────────
        self.play(FadeOut(warn_grp, rate_func=smooth_step_in_out), run_time=0.8)
        sc_pts = [LEFT*4.0+DOWN*1.5, LEFT*1.5+DOWN*0.5,
                  RIGHT*1.0+UP*0.8,  RIGHT*4.0+UP*1.8]
        sc_curve = CubicBezier(*sc_pts, color=AMBER, stroke_width=3.0)
        sc_lbl   = self._t("Quy luật mở rộng (Scaling Laws)", size=15,
                             color=AMBER).shift(RIGHT*2.5 + UP*2.8)
        self.play(Create(sc_curve), Write(sc_lbl,
                                          rate_func=smooth_step_in_out), run_time=2.0)
        self.wait(5.9)

        # ── [03:12.4 – 03:20.9] Dự đoán Reference Loss ───────────────────────
        ref_l1 = DashedLine(LEFT*2.5+UP*0.6, LEFT*0.5+UP*0.6,
                             color=AMBER, stroke_width=2.0)
        ref_l2 = DashedLine(RIGHT*0.5+DOWN*0.6, RIGHT*2.5+DOWN*0.6,
                             color=AMBER, stroke_width=2.0)
        ref_lbl2 = self._t("Reference Loss dự đoán", size=13,
                             color=AMBER).shift(RIGHT*2.5 + UP*2.0)
        self.play(Create(ref_l1), Create(ref_l2),
                  Write(ref_lbl2, rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(7.3)

        # ── [03:20.9 – 03:31.3] Cân bằng Loss hoàn hảo ──────────────────────
        self.play(FadeOut(VGroup(sc_curve, sc_lbl),
                          rate_func=smooth_step_in_out), run_time=0.8)
        target_h = 1.2
        self.play(
            bar_c4.animate.stretch_to_fit_height(target_h).set_y(-1.4),
            bar_gh.animate.stretch_to_fit_height(target_h).set_y(-1.4),
            rate_func=smooth_step_in_out, run_time=1.8
        )
        mix_p = self._panel(8.4, 0.82, TEAL)
        mix_l = self._t("Domain Mixtures tối ưu  →  Hiệu suất tăng vọt",
                         size=18, color=TEAL, bold=True).move_to(mix_p)
        mix_grp = VGroup(mix_p, mix_l).shift(UP*0.8)

        self.play(FadeIn(mix_grp, scale=0.88,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(6.3)
        self.play(FadeOut(VGroup(loss_hdr, loss_hdr_l, base_ln,
                                  bar_c4, lbl_c4, bar_gh, lbl_gh,
                                  ref_l1, ref_l2, ref_lbl2, mix_grp),
                          rate_func=smooth_step_in_out), run_time=1.5)

        # ── [03:31.3 – 03:42.2] Kết quả Sheared LLaMA ───────────────────────
        res_hdr  = self._panel(8.4, 0.7, TEAL).to_edge(UP, buff=0.3)
        res_hdr_l = self._t("KẾT QUẢ : SHEARED LLAMA",
                              size=22, color=TEAL, bold=True).move_to(res_hdr)

        m1b = self._panel(4.2, 1.0, BLUE).shift(LEFT*2.5 + UP*0.7)
        m1b_l = self._t("Sheared LLaMA  1B", size=19,
                          color=BLUE, bold=True).move_to(m1b)
        m3b = self._panel(4.2, 1.0, BLUE).shift(RIGHT*2.5 + UP*0.7)
        m3b_l = self._t("Sheared LLaMA  3B", size=19,
                          color=BLUE, bold=True).move_to(m3b)

        self.play(FadeIn(VGroup(res_hdr, res_hdr_l),
                         rate_func=smooth_step_in_out), run_time=0.8)
        self.play(
            FadeIn(VGroup(m1b, m1b_l), shift=UP*0.2,
                   rate_func=smooth_step_in_out),
            FadeIn(VGroup(m3b, m3b_l), shift=UP*0.2,
                   rate_func=smooth_step_in_out),
            run_time=1.5
        )
        self.wait(7.1)

        # ── [03:42.2 – 03:56.1] Chi phí rẻ ──────────────────────────────────
        stats = VGroup(
            self._t("Dữ liệu :  50 Tỷ Tokens",                   size=16, color=TEXT),
            self._t("Điện toán :  3% so với huấn luyện từ đầu",   size=16, color=TEXT),
            self._t("Thời gian :  8 GPU  /  2–3 Ngày",            size=16, color=AMBER, bold=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).shift(DOWN*0.7)
        self.play(LaggedStart(*[Write(s, rate_func=smooth_step_in_out)
                                for s in stats], lag_ratio=0.4), run_time=2.5)
        self.wait(11.4)

        # ── [03:56.1 – 04:07.3] SOTA ─────────────────────────────────────────
        sota_p = self._panel(5.2, 1.1, AMBER)
        sota_p.set_fill(color="#2A1A00")
        sota_l = self._t("👑  NGÔI VƯƠNG SOTA", size=27,
                          color=AMBER, bold=True).move_to(sota_p)
        sota_grp = VGroup(sota_p, sota_l).shift(UP*1.8)

        self.play(FadeIn(sota_grp, scale=1.25,
                         rate_func=bounce), run_time=1.5)   # bounce → cảm giác "đăng quang"
        self.play(FadeOut(stats, rate_func=smooth_step_in_out), run_time=1.2)
        self.wait(8.5)

        # ── [04:07.3 – 04:16.0] Số lượt tải ─────────────────────────────────
        hf_p = self._panel(6.2, 0.88, TEAL)
        hf_l = self._t("Hugging Face :  800.000+  Downloads",
                        size=19, color=TEAL, bold=True).move_to(hf_p)
        hf_grp = VGroup(hf_p, hf_l).shift(DOWN*1.1)

        self.play(Write(hf_l, rate_func=smooth_step_in_out),
                  FadeIn(hf_p, rate_func=smooth_step_in_out), run_time=1.2)
        self.play(
            VGroup(m1b, m1b_l).animate.scale(1.25).shift(LEFT*0.7),
            VGroup(m3b, m3b_l).animate.scale(0.78).shift(RIGHT*0.5),
            rate_func=smooth_step_in_out, run_time=2.0
        )
        self.wait(5.5)

        # ── [04:16.0 – 04:33.7] Công nghiệp áp dụng ─────────────────────────
        self.play(FadeOut(VGroup(sota_grp, hf_grp),
                          rate_func=smooth_step_in_out), run_time=1.0)
        self.play(
            VGroup(m1b, m1b_l).animate.scale(0.6).shift(LEFT*0.5),
            VGroup(m3b, m3b_l).animate.scale(0.75).shift(LEFT*0.5),
            rate_func=smooth_step_in_out, run_time=1.5
        )

        nvidia_l = self._t("NVIDIA Miniature",               size=17, color=ROSE, bold=True).shift(RIGHT*3.5 + UP*1.4)
        meta_l   = self._t("Meta Llama 3.2 & 3.3\n(Cắt tỉa từ 8B/70B)", size=17, color=ROSE, bold=True).shift(RIGHT*3.5 + DOWN*0.5)
        ind_arr  = Arrow(m3b.get_right(), meta_l.get_left(),
                         color=TEAL, stroke_width=3.5, buff=0.12)

        self.play(
            FadeIn(VGroup(nvidia_l, meta_l), shift=LEFT*0.2,
                   rate_func=smooth_step_in_out),
            GrowArrow(ind_arr),
            run_time=2.0
        )
        self.wait(13.2)

        # ── [04:33.7 – 04:58.8] Giới hạn Qwen → câu hỏi kế tiếp ─────────────
        self.play(
            FadeOut(VGroup(res_hdr, res_hdr_l,
                           m1b, m1b_l, m3b, m3b_l,
                           nvidia_l, meta_l, ind_arr),
                    rate_func=smooth_step_in_out),
            run_time=1.2
        )

        qwen_p = self._panel(8.4, 2.2, ROSE)
        qwen_p.set_fill(color="#1A0A0A")
        qwen_c = VGroup(
            self._t("Qwen 2.5  3B", size=23, color=ROSE, bold=True),
            self._t("Huấn luyện trên  18 NGHÌN TỶ TOKEN", size=18, color=TEXT),
            self._t("[X]  Vượt xa ngân sách học thuật", size=17, color=ROSE, bold=True),
        ).arrange(DOWN, buff=0.28).move_to(qwen_p)
        qwen_grp = VGroup(qwen_p, qwen_c)

        self.play(FadeIn(qwen_grp, scale=0.88,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(3.8)
        self.play(FadeOut(qwen_grp, rate_func=smooth_step_in_out), run_time=0.9)

        next_p = self._panel(9.4, 1.8, AMBER)
        next_p.set_fill(color="#1A1000")
        next_l = self._t(
            '"DỮ LIỆU TỔNG HỢP (SYNTHETIC DATA)\nCÓ PHẢI LÀ TƯƠNG LAI?"',
            size=22, color=AMBER, bold=True
        ).move_to(next_p)
        next_grp = VGroup(next_p, next_l)

        self.play(FadeIn(next_grp, scale=0.88,
                         rate_func=smooth_step_in_out), run_time=1.5)
        self.wait(15.0)
        self.play(FadeOut(next_grp, rate_func=smooth_step_in_out), run_time=1.2)


FullVideoBase = P4_Complete if P4_Complete is not None else S1_Intro


class FullVideo(FullVideoBase):
    """Render Part 1 through Part 5 into one continuous video."""

    # Part 1-3 expect these S1 helpers on self. P4_Complete supplies the
    # VoiceoverScene functionality required by Part 4 and Part 5.
    _t = S1_Intro._t
    _panel = S1_Intro._panel
    _pill = S1_Intro._pill
    _industry_block = S1_Intro._industry_block
    _label_panel = S1_Intro._label_panel

    def construct(self):
        if PARTS_IMPORT_ERROR is not None:
            raise RuntimeError(
                "Cannot render Part 4 and Part 5. Check the files in the "
                "'manim' folder and install the packages in requirements.txt."
            ) from PARTS_IMPORT_ERROR

        S1_Intro.construct(self)
        self.clear()

        S2_LLMBoom.construct(self)
        self.clear()

        S3_WhyMatters.construct(self)
        self.clear()

        P4_Complete.construct(self)
        self.clear()

        P5_Complete.construct(self)


if __name__ == "__main__":
    quality = os.environ.get("MANIM_QUALITY", "-ql")

    print(f"Exporting FullVideo with quality {quality}...")
    subprocess.run(
        [sys.executable, "-m", "manim", quality, __file__, "FullVideo"],
        check=True,
    )

