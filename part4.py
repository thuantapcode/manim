"""
Phần 4: Dữ liệu Pre-training & Post-training Alignment — v5 (CSV-aligned rewrite)
Manim Community v0.20.1 | Voice: vi-VN-NamMinhNeural
Render: manim -pqh part4.py <ClassName>
"""
from __future__ import annotations
import sys, os
import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene
from pyglet.window.mouse import MIDDLE

sys.path.insert(0, os.path.dirname(__file__))
from edge_service import EdgeTTSService

# ── Constants ─────────────────────────────────────────────────────────────────
FONT      = "Be Vietnam Pro"
ACADEMIA  = BLUE_C
INDUSTRY  = RED_C
HIGHLIGHT = YELLOW_C
SUCCESS   = GREEN_C
NEUTRAL   = GRAY_C
VOICE     = "vi-VN-NamMinhNeural"

# ── Global helpers ────────────────────────────────────────────────────────────
def svc():
    return EdgeTTSService(voice=VOICE)


def T(text, font_size=24, color=WHITE, **kw):
    return Text(text, font=FONT, font_size=font_size, color=color, **kw)


def title_card(text, color=ACADEMIA, size=34):
    return Text(text, font=FONT, font_size=size, color=color, weight=BOLD)


def clear(scene, run_time=0.5):
    mobs = [m for m in scene.mobjects]
    if mobs:
        scene.play(*[FadeOut(m, run_time=run_time) for m in mobs], run_time=run_time)


def flash_mob(scene, mob, color=HIGHLIGHT, radius=0.6):
    scene.play(Flash(mob, color=color, flash_radius=radius, num_lines=14), run_time=0.5)


def build_radar_axes(center=ORIGIN, radius=1.8,
                     labels=("Phong cách", "Xác thực", "Giáo dục", "Chuyên môn"),
                     label_offset=0.45):
    n = len(labels)
    ctr = np.array(center, dtype=float) if not isinstance(center, np.ndarray) \
          else center.astype(float)
    group = VGroup()
    for level in (.25, .5, .75, 1.0):
        pts = [ctr + radius * level
               * np.array([np.cos(2*PI*i/n - PI/2), np.sin(2*PI*i/n - PI/2), 0])
               for i in range(n)]
        group.add(Polygon(*pts, color=GRAY_C, stroke_width=.6,
                          fill_opacity=0, stroke_opacity=.4))
    tips = []
    for i, lbl in enumerate(labels):
        ang = 2*PI*i/n - PI/2
        tip = ctr + radius * np.array([np.cos(ang), np.sin(ang), 0])
        tips.append(tip)
        group.add(Line(ctr, tip, color=GRAY_B, stroke_width=1))
        offset = label_offset * np.array([np.cos(ang), np.sin(ang), 0])
        lmob = Text(lbl, font=FONT, font_size=13, color=WHITE)
        lmob.move_to(tip + offset)
        group.add(lmob)
    return group, tips


def build_radar_poly(vals, tips, center=None, color=ACADEMIA):
    ctr = np.array(center, dtype=float) if center is not None \
          else np.array([0.0, 0.0, 0.0])
    pts = [ctr + (np.array(tip) - ctr) * v for tip, v in zip(tips, vals)]
    return Polygon(*pts, color=color, fill_color=color,
                   fill_opacity=.28, stroke_width=2.5)


def chapter_break(scene, title, subtitle=None, color=ACADEMIA):
    """
    Cinematic chapter-break card (~1.8 s).
    Must be called when the screen is already empty (after clear()).
    Layout: horizontal accent bar  ·  title above  ·  subtitle below
    Exit: whole card slides out to the right (film-wipe feel).
    """
    bar     = Line(LEFT * 4.4, RIGHT * 4.4, color=color, stroke_width=2.8)
    title_m = T(title, 26, WHITE, weight=BOLD)
    title_m.next_to(bar, UP, buff=0.28)

    items = [bar, title_m]
    if subtitle:
        sub_m = T(subtitle, 14, color)
        sub_m.next_to(bar, DOWN, buff=0.22)
        items.append(sub_m)

    # Animate IN ──────────────────────────────────────────────────────────
    scene.play(GrowFromCenter(bar), run_time=0.35)
    scene.play(FadeIn(title_m, shift=DOWN * 0.10), run_time=0.38)
    if subtitle:
        scene.play(FadeIn(sub_m, shift=UP * 0.07), run_time=0.28)
    scene.wait(0.52)

    # Animate OUT — slide to the right (film wipe) ────────────────────────
    scene.play(
        VGroup(*items).animate.shift(RIGHT * 12),
        run_time=0.38, rate_func=rush_into,
    )
    scene.remove(*items)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — P4_DataCuration
# ══════════════════════════════════════════════════════════════════════════════
class P4_DataCuration(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ─────────────────────────────────────────────────────────────
        # INTRO
        # ─────────────────────────────────────────────────────────────
        badge_bg = RoundedRectangle(
            corner_radius=0.2,
            width=9,
            height=1.05,
            color=ACADEMIA,
            fill_color=ACADEMIA,
            fill_opacity=0.12,
            stroke_width=2,
        )

        badge_txt = title_card(
            "PRE-TRAINING DATA CURATION",
            size=28
        )

        header = VGroup(
            badge_bg,
            badge_txt
        ).shift(UP * 2.7)

        with self.voiceover(
                text=(
                        "Sau khi bàn về quy mô mô hình, chúng ta sẽ chuyển sang một mặt trận khác "
                        "đang ngày càng được xem là yếu tố quyết định thành công của các hệ thống AI hiện đại: "
                        "quản lý và tuyển chọn dữ liệu tiền huấn luyện."
                )
        ) as tr:

            self.play(
                FadeIn(header, shift=DOWN * 0.2),
                run_time=min(1.2, tr.duration * 0.25)
            )

            self.wait(max(0, tr.duration - 1.3))

        # ─────────────────────────────────────────────────────────────
        # DATA CLEANING WAS UNDERRATED
        # ─────────────────────────────────────────────────────────────

        raw_box = RoundedRectangle(
            corner_radius=0.12,
            width=2.4,
            height=0.9,
            fill_color=GRAY_C,
            fill_opacity=0.12,
        )

        raw_label = T(
            "Dữ liệu thô",
            16,
            GRAY_A
        )

        raw_group = VGroup(
            raw_box,
            raw_label
        )

        clean_box = RoundedRectangle(
            corner_radius=0.12,
            width=2.8,
            height=0.9,
            fill_color=NEUTRAL,
            fill_opacity=0.12,
            stroke_color=NEUTRAL,
        )

        clean_label = T(
            "Data Cleaning",
            18,
            NEUTRAL,
            weight=BOLD
        )

        clean_group = VGroup(
            clean_box,
            clean_label
        )

        quality_box = RoundedRectangle(
            corner_radius=0.12,
            width=2.8,
            height=0.9,
            fill_color=SUCCESS,
            fill_opacity=0.12,
            stroke_color=SUCCESS,
        )

        quality_label = T(
            "Hiệu năng LLM",
            18,
            SUCCESS,
            weight=BOLD
        )

        quality_group = VGroup(
            quality_box,
            quality_label
        )

        pipeline = VGroup(
            raw_group,
            clean_group,
            quality_group
        ).arrange(
            RIGHT,
            buff=1.0
        )

        pipeline.move_to(DOWN * 0.4)

        a1 = Arrow(
            raw_group.get_right(),
            clean_group.get_left(),
            buff=0.15
        )

        a2 = Arrow(
            clean_group.get_right(),
            quality_group.get_left(),
            buff=0.15
        )

        wrong_tag = T(
            "Bị xem là công việc phụ",
            16,
            INDUSTRY
        )

        wrong_tag.next_to(
            clean_group,
            UP,
            buff=0.25
        )

        cross = Cross(
            clean_group,
            stroke_color=INDUSTRY,
            stroke_width=6
        )

        with self.voiceover(
                text=(
                        "Trong nhiều năm, việc dọn dẹp dữ liệu thường bị xem như một công việc hậu cần đơn thuần, "
                        "một bước xử lý phụ trước khi huấn luyện mô hình."
                )
        ) as tr:

            self.play(
                FadeIn(raw_group)
            )

            self.play(
                GrowArrow(a1)
            )

            self.play(
                FadeIn(clean_group)
            )

            self.play(
                FadeIn(wrong_tag)
            )

            self.play(
                Create(cross)
            )

            self.wait(max(0, tr.duration - 4))

        with self.voiceover(
                text=(
                        "Nhưng thực tế lại hoàn toàn ngược lại. "
                        "Chất lượng của bước làm sạch dữ liệu có ảnh hưởng trực tiếp đến hiệu năng cuối cùng của mô hình."
                )
        ) as tr:

            self.play(
                FadeOut(cross),
                FadeOut(wrong_tag)
            )

            self.play(
                GrowArrow(a2)
            )

            self.play(
                FadeIn(quality_group)
            )

            self.play(
                Indicate(
                    clean_group,
                    color=HIGHLIGHT,
                    scale_factor=1.08
                )
            )

            self.play(
                Indicate(
                    quality_group,
                    color=SUCCESS,
                    scale_factor=1.08
                )
            )

            self.wait(max(0, tr.duration - 2.5))

        self.play(
            FadeOut(
                VGroup(
                    pipeline,
                    a1,
                    a2
                )
            )
        )

        # ─────────────────────────────────────────────────────────────
        # QUALITY > QUANTITY
        # ─────────────────────────────────────────────────────────────

        qty = T("SỐ LƯỢNG", 38, GRAY_C, weight=BOLD)
        gt = T(">", 38, WHITE, weight=BOLD)
        qual = T("CHẤT LƯỢNG", 44, HIGHLIGHT, weight=BOLD)

        expr = VGroup(
            qual,
            gt,
            qty
        ).arrange(RIGHT, buff=0.25)

        with self.voiceover(
                text=(
                        "Ngày nay, ngày càng nhiều bằng chứng cho thấy chất lượng dữ liệu "
                        "quan trọng hơn rất nhiều so với việc chỉ tiếp tục tăng số lượng dữ liệu."
                )
        ) as tr:

            self.play(
                FadeIn(qty, scale=0.7)
            )

            self.play(
                FadeIn(gt)
            )

            self.play(
                GrowFromCenter(qual)
            )

            flash_mob(
                self,
                qual,
                radius=0.8
            )

            self.wait(max(0, tr.duration - 2))

        self.play(FadeOut(expr))

        # ─────────────────────────────────────────────────────────────
        # WHY ACADEMIA
        # ─────────────────────────────────────────────────────────────

        # ── 1.4 Why academia? ─────────────────────────────────────────────────
        why_q = T("Tại sao giới học thuật lại nên dấn thân vào cuộc đua dữ liệu này?", 20, HIGHLIGHT)
        why_q.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
                text="Vậy, tại sao giới học thuật lại nên dấn thân vào cuộc đua dữ liệu này?"
        ) as tr:
            self.play(FadeIn(why_q, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0, tr.duration - 0.7))

        # Answer: small → large scale transfer
        ans_grp = VGroup(
            T("↑ Thực nghiệm quy mô nhỏ", 24, SUCCESS, weight=BOLD),
            T("↕  chuyển giao hiệu quả", 20, WHITE),
            T("↓ Hệ thống quy mô lớn", 24, SUCCESS, weight=BOLD),
        ).arrange(DOWN, buff=0.3)
        ans_grp.move_to(DOWN * 0.75)

        with self.voiceover(
                text="Câu trả lời là vì đây là hướng đi triển vọng nhất, nơi những thực nghiệm ở "
                     "quy mô nhỏ hoàn toàn có thể chuyển giao và ứng dụng hiệu quả cho các hệ thống "
                     "quy mô lớn hơn."
        ) as tr:
            self.play(
                LaggedStart(*[FadeIn(a, shift=RIGHT * 0.15) for a in ans_grp],
                            lag_ratio=0.3),
                run_time=min(1.4, tr.duration * 0.6)
            )
            self.wait(max(0, tr.duration - 1.7))

        self.play(FadeOut(VGroup(why_q, ans_grp)))

        # ─────────────────────────────────────────────────────────────
        # DC-LM
        # ─────────────────────────────────────────────────────────────

        title = T(
            "DC-LM: Thứ hạng ổn định trên mọi quy mô",
            20
        )

        title.next_to(header, DOWN, buff=0.45)

        scales = ["100M", "1B", "10B"]

        columns = VGroup()

        for i, scale in enumerate(scales):
            col = VGroup(
                T(scale, 16, HIGHLIGHT, weight=BOLD),
                T("#1 Dataset A", 15, SUCCESS),
                T("#2 Dataset B", 15, ACADEMIA),
                T("#3 Dataset C", 15, NEUTRAL),
            ).arrange(DOWN, buff=0.22)

            col.move_to(
                np.array([-3 + i * 3, -0.3, 0])
            )

            columns.add(col)

        with self.voiceover(
                text=(
                        "Cuộc thi DC LM cho thấy một kết quả rất đáng chú ý. "
                        "Những tập dữ liệu tốt nhất ở quy mô nhỏ thường vẫn là những tập dữ liệu tốt nhất "
                        "khi quy mô mô hình tăng lên."
                )
        ) as tr:

            self.play(FadeIn(title))

            self.play(
                LaggedStart(
                    *[FadeIn(c) for c in columns],
                    lag_ratio=0.3
                )
            )

            for c in columns:
                self.play(
                    Indicate(c[1], color=SUCCESS),
                    run_time=0.4
                )

            self.wait(max(0, tr.duration - 3))

        self.play(
            FadeOut(title),
            FadeOut(columns)
        )

        # ── 1.6 Budget check ─────────────────────────────────────────────────
        budget_check = T("Kiểm tra thực tế: Ngân sách học thuật", 20, WHITE)
        budget_check.next_to(header, DOWN, buff=0.45)

        with self.voiceover(
                text="Một kiểm tra thực tế nhanh cho thấy: cấu hình nghiên cứu dữ liệu hoàn toàn "
                     "nằm trong tầm tay của ngân sách học thuật."
        ) as tr:
            self.play(FadeIn(budget_check, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0, tr.duration - 0.8))

        # ── 1.7 8 GPU recipe ─────────────────────────────────────────────────
        gpus = VGroup(*[
            Square(side_length=0.50,
                   fill_color=ACADEMIA, fill_opacity=0.28,
                   stroke_color=ACADEMIA, stroke_width=2)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.12)
        gpus.move_to(UP * 1.1)

        gpu_t = T("8 GPU", 30, ACADEMIA, weight=BOLD)
        x_t = T("×", 26, WHITE)
        day_t = T("< 1 ngày", 30, HIGHLIGHT, weight=BOLD)
        eq_t = T("→", 24, WHITE)
        res_t = T("Mô hình 1B / 30B token", 24, SUCCESS, weight=BOLD)
        formula = VGroup(gpu_t, x_t, day_t, eq_t, res_t).arrange(RIGHT, buff=0.22)
        formula.move_to(DOWN * 0.05)

        cap_t = T("→ Đóng góp khoa học có sức nặng!", 18, GRAY_A)
        cap_t.move_to(DOWN * 0.85)

        with self.voiceover(
                text="Với thông lệ phổ biến là huấn luyện mô hình 1 tỷ tham số (1B) trên gần 30 tỷ token, "
                     "chúng ta chỉ cần dùng khoảng 8 GPU chạy trong chưa đầy một ngày là đã có thể "
                     "tạo ra những đóng góp khoa học có sức nặng."
        ) as tr:
            self.play(
                LaggedStart(*[GrowFromCenter(g) for g in gpus], lag_ratio=0.08),
                run_time=1.2
            )
            self.play(FadeIn(formula), run_time=0.7)
            self.play(FadeIn(cap_t), run_time=0.5)
            self.wait(max(0, tr.duration - 2.7))

        self.play(FadeOut(VGroup(budget_check, gpus, formula, cap_t)))

        # ── 1.8 Open source community ─────────────────────────────────────────
        os_t = T("Cộng đồng mã nguồn mở hạ thấp rào cản nghiên cứu", 20, SUCCESS, weight=BOLD)
        os_t.next_to(header, DOWN, buff=0.45)

        with self.voiceover(
                text="Bước đệm lớn nhất giúp hạ thấp rào cản nghiên cứu này chính là những nỗ lực "
                     "không mệt mỏi từ cộng đồng mã nguồn mở."
        ) as tr:
            self.play(FadeIn(os_t, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0, tr.duration - 0.7))

        # ── 1.9 Dataset timeline ─────────────────────────────────────────────
        ds_data = [
            ("RedPajama", "2023", "1.2T token", ACADEMIA),
            ("DOMA (AI2)", "2023", "OLMo corpus", INDUSTRY),
            ("DC-LM", "2024", "Common Crawl", SUCCESS),
        ]
        cards = VGroup()
        for name, yr, size, col in ds_data:
            card_bg = RoundedRectangle(corner_radius=0.12, width=5.8, height=0.68,
                                       fill_color=col, fill_opacity=0.10,
                                       stroke_color=col, stroke_width=1.5)
            nm_t = T(name, 18, col, weight=BOLD)
            inf_t = T(f"{yr}  ·  {size}", 14, GRAY_A)
            nm_t.move_to([-1.4, 0, 0])
            inf_t.move_to([1.2, 0, 0])
            cards.add(VGroup(card_bg, nm_t, inf_t))
        cards.arrange(DOWN, buff=0.20).move_to(DOWN * 0.65)

        with self.voiceover(
                text="Từ sự xuất hiện của Red Pyjama, tập dữ liệu DOMA của viện AI2 vào năm 2023, "
                     "cho đến cuộc thi Datacom LLM với bể dữ liệu DC-LM khổng lồ trích xuất từ "
                     "Common Crawl... Tất cả đã tạo ra một bệ phóng vững chắc để phần còn lại của "
                     "cộng đồng đẩy biên giới tri thức tiến về phía trước."
        ) as tr:
            self.play(
                LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cards],
                            lag_ratio=0.3),
                run_time=min(1.6, tr.duration * 0.55)
            )
            self.wait(max(0, tr.duration - 2.0))

        self.play(FadeOut(VGroup(os_t, cards)))

        # ── 1.10 Research question ────────────────────────────────────────────
        rq_t = T("Làm thế nào để đo lường và lựa chọn dữ liệu\ndựa trên các tín hiệu chất lượng?",
                 20, HIGHLIGHT)
        rq_t.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
                text="Khi đã có trong tay những tập dữ liệu tương đối sạch, câu hỏi nghiên cứu tiếp "
                     "theo là: Làm thế nào để đo lường và lựa chọn dữ liệu dựa trên các tín hiệu "
                     "chất lượng?"
        ) as tr:
            self.play(FadeIn(rq_t, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0, tr.duration - 0.8))

        self.play(FadeOut(rq_t))
        # =====================================================================
        # MODEL-BASED QUALITY FILTERING (Fix lỗi đè hạt 2D & trùng lặp đối tượng)
        # =====================================================================
        filt_title = T(
            "Model-Based Quality Filtering",
            24,
            WHITE,
            weight=BOLD
        ).next_to(header, DOWN, buff=0.4)

        base_y_boxes = 0.4

        raw_bg = RoundedRectangle(
            width=2.2, height=0.7, corner_radius=0.1,
            fill_color=NEUTRAL, fill_opacity=0.12, stroke_color=NEUTRAL
        )
        raw_t = T("Dữ liệu thô", 14, NEUTRAL)
        raw_grp = VGroup(raw_bg, raw_t).move_to(LEFT * 4.3 + UP * base_y_boxes)
        raw_t.move_to(raw_bg.get_center())

        model_bg = RoundedRectangle(
            width=2.8, height=0.7, corner_radius=0.1,
            fill_color=HIGHLIGHT, fill_opacity=0.12, stroke_color=HIGHLIGHT
        )
        model_t = T("Mô hình đánh giá", 14, HIGHLIGHT)
        model_grp = VGroup(model_bg, model_t).move_to(UP * base_y_boxes)
        model_t.move_to(model_bg.get_center())

        clean_bg = RoundedRectangle(
            width=2.2, height=0.7, corner_radius=0.1,
            fill_color=SUCCESS, fill_opacity=0.12, stroke_color=SUCCESS
        )
        clean_t = T("Dữ liệu sạch", 14, SUCCESS)
        clean_grp = VGroup(clean_bg, clean_t).move_to(RIGHT * 4.3 + UP * base_y_boxes)
        clean_t.move_to(clean_bg.get_center())

        a1 = Arrow(raw_bg.get_right(), model_bg.get_left(), buff=0.08, color=GRAY_B,
                   max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(model_bg.get_right(), clean_bg.get_left(), buff=0.08, color=GRAY_B,
                   max_tip_length_to_length_ratio=0.15)

        methods = VGroup(
            T("AskLLM (Google)", 13, ACADEMIA, weight=BOLD),
            T("FineWeb-Edu (HF)", 13, SUCCESS, weight=BOLD),
        ).arrange(DOWN, buff=0.1).next_to(filt_title, DOWN, buff=0.24)

        with self.voiceover(
                text="Một hướng tiếp cận đang phát triển rất nhanh là sử dụng chính các mô hình ngôn ngữ "
                     "để đánh giá chất lượng dữ liệu."
        ) as tr:
            self.play(FadeIn(filt_title))
            self.play(FadeIn(raw_grp), FadeIn(model_grp), FadeIn(clean_grp), FadeIn(methods), run_time=0.9)
            self.play(Create(a1), Create(a2), run_time=0.5)
            self.wait(max(0.1, tr.duration - 1.4))

        raw_docs = VGroup()
        card_width = 0.45
        card_height = 0.3
        h_gap = 0.55  # khoảng cách tâm theo chiều ngang (lớn hơn chiều rộng)
        v_gap = 0.4  # khoảng cách tâm theo chiều dọc (lớn hơn chiều cao)

        cols = 4
        rows = 3
        # Tính toán vị trí bắt đầu để lưới cân đối quanh gốc (0,0)
        start_x = - (cols - 1) * h_gap / 2
        start_y = (rows - 1) * v_gap / 2

        data_y = -1.2  # bạn có thể thay đổi giá trị này

        for i in range(12):
            row = i // cols
            col = i % cols
            x = start_x + col * h_gap
            y = start_y - row * v_gap  # vì y giảm dần khi xuống hàng dưới
            card = RoundedRectangle(
                width=card_width, height=card_height, corner_radius=0.04,
                fill_color=GRAY_B, fill_opacity=0.35,
                stroke_color=GRAY_B, stroke_width=1
            )
            card.move_to(LEFT * 4.3 + UP * data_y + RIGHT * x + UP * y)
            raw_docs.add(card)

        with self.voiceover(
                text="Hãy tưởng tượng chúng ta bắt đầu với một kho dữ liệu khổng lồ, "
                     "trong đó có cả nội dung chất lượng cao lẫn rất nhiều nhiễu."
        ) as tr:
            self.play(
                LaggedStart(*[FadeIn(doc, scale=0.8) for doc in raw_docs], lag_ratio=0.04),
                run_time=0.8
            )
            self.wait(max(0.1, tr.duration - 0.8))

        # Tịnh tiến nguyên vẹn lưới ma trận 2D thô vào trục xử lý trung tâm
        with self.voiceover(
                text="Toàn bộ dữ liệu được đưa qua một mô hình đánh giá chất lượng."
        ) as tr:
            self.play(
                raw_docs.animate.shift(RIGHT * 4.3),
                run_time=1.2,
                rate_func=smooth
            )
            self.wait(max(0.1, tr.duration - 1.2))

        # Thiết lập tia quét laser chấm điểm dữ liệu
        score_label = T("Quality Scoring", 15, HIGHLIGHT, weight=BOLD).move_to(UP * (data_y + 0.7))
        scan_line = DashedLine(model_bg.get_bottom(), score_label.get_top(), color=HIGHLIGHT, stroke_width=2)

        with self.voiceover(
                text="Mô hình sẽ chấm điểm từng tài liệu dựa trên độ hữu ích, "
                     "mức độ nhất quán và giá trị học tập của nội dung."
        ) as tr:
            self.play(Create(scan_line), FadeIn(score_label, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(model_grp, color=HIGHLIGHT, scale_factor=1.04), run_time=0.6)
            self.wait(max(0.1, tr.duration - 1.1))

        # Lọc dữ liệu thông minh: Phân tách đan xen phần tử nhiễu và sạch để phân bố 2D đều đẹp
        # Chọn các vị trí hạt ngẫu nhiên [0, 2, 5, 11] làm hạt tốt để giữ dáng lưới 2 chiều
        good_indices = [0, 3, 6, 9]
        bad_docs = VGroup(*[raw_docs[i] for i in range(12) if i not in good_indices])
        good_docs = VGroup(*[raw_docs[i] for i in range(12) if i in good_indices])

        crosses = VGroup()
        for doc in bad_docs:
            c = Cross(doc, color=RED_C, stroke_width=3.5).scale(0.85)
            crosses.add(c)

        with self.voiceover(
                text="Phần lớn dữ liệu sẽ bị loại bỏ vì chất lượng thấp, "
                     "trùng lặp hoặc chứa quá nhiều nhiễu."
        ) as tr:
            self.play(
                *[doc.animate.set_fill(RED_C, opacity=0.4).set_stroke(RED_C) for doc in bad_docs],
                run_time=0.6
            )
            self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.04), run_time=0.8)
            self.wait(max(0.1, tr.duration - 1.4))

        with self.voiceover(
                text="Chỉ một phần nhỏ được giữ lại để trở thành dữ liệu huấn luyện chất lượng cao."
        ) as tr:
            # Triệt tiêu hoàn toàn hạt lỗi và laser
            self.play(FadeOut(bad_docs), FadeOut(crosses), FadeOut(scan_line), run_time=0.6)

            # Hạt tốt hóa xanh lục và bừng sáng tại chỗ
            self.play(
                *[doc.animate.set_fill(SUCCESS, opacity=0.7).set_stroke(SUCCESS).scale(1.1) for doc in good_docs],
                run_time=0.6
            )
            self.wait(max(0.1, tr.duration - 1.2))

        self.play(FadeOut(good_docs, run_time=0.1))

        # Khởi tạo ma trận dữ liệu sạch mới tinh đã RE-SHAPE thành lưới 2 chiều 2x2 cực kỳ thoáng đãng
        clean_docs = VGroup()
        for _ in range(4):
            card = RoundedRectangle(
                width=0.45, height=0.3, corner_radius=0.04,
                fill_color=SUCCESS, fill_opacity=0.7,
                stroke_color=SUCCESS, stroke_width=1.2
            ).scale(1.1)
            clean_docs.add(card)

        # Sắp xếp 4 hạt thành mạng lưới 2 hàng x 2 cột, giãn cách 0.35 đơn vị rất ngăn nắp
        clean_docs.arrange_in_grid(rows=2, cols=2, buff=0.35)
        # Đặt điểm xuất phát tại trung tâm xử lý (X=0, Y=-1.2)
        clean_docs.move_to(UP * data_y)

        self.play(FadeIn(clean_docs, scale=0.9), run_time=0.3)

        with self.voiceover(
                text="Kết quả cuối cùng là một tập dữ liệu nhỏ hơn rất nhiều, "
                     "nhưng giàu thông tin hơn và hiệu quả hơn cho quá trình huấn luyện."
        ) as tr:
            # Tịnh tiến nguyên khối lưới 2x2 sang kho lưu trữ bên phải mà không lo co cụm hay chồng lấn
            self.play(
                clean_docs.animate.shift(RIGHT * 4.3),
                run_time=1.3,
                rate_func=smooth
            )

            # Pháo hoa kích nổ chuẩn tâm 100% tại điểm neo của khối dữ liệu sạch vừa dừng chân
            self.play(Flash(clean_docs.get_center(), color=SUCCESS, flash_radius=0.7, num_lines=10), run_time=0.5)
            self.wait(max(0.1, tr.duration - 2.1))

        # Dọn dẹp mượt mà toàn bộ phân cảnh chuẩn bị chuyển cảnh tiếp theo
        self.play(
            FadeOut(VGroup(
                filt_title, raw_grp, model_grp, clean_grp,
                a1, a2, methods, clean_docs, score_label
            )),
            run_time=0.6
        )
        self.wait(0.2)
        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — P4_CuratingProject
# ══════════════════════════════════════════════════════════════════════════════
class P4_CuratingProject(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ── Header cố định ─────────────────────────────────────────────────────
        hdr_bg  = RoundedRectangle(
            corner_radius=0.15, width=9.6, height=0.72,
            color=ACADEMIA, fill_color=ACADEMIA,
            fill_opacity=0.12, stroke_width=1.5
        )
        hdr_txt = title_card("DỰ ÁN: Curating  |  Danqi Chen  |  ICLR 2024", size=22)
        header  = VGroup(hdr_bg, hdr_txt).move_to(UP * 2.7)

        ref_lbl = T("Lin et al., ICLR 2024", 13, NEUTRAL)
        ref_lbl.to_corner(DR).shift(LEFT * 0.3 + DOWN * 0.12)

        # ═══════════════════════════════════════════════════════════════════════
        # VO1 — LM Pairwise Judge  (01:43–01:54, ~11s)
        # ═══════════════════════════════════════════════════════════════════════
        def make_doc_card(label_text, accent):
            bg = RoundedRectangle(
                corner_radius=0.12, width=2.3, height=3.0,
                fill_color="#0b0f1a", fill_opacity=1.0,
                stroke_color=accent, stroke_width=2.2
            )
            lbl = T(label_text, 18, accent, weight=BOLD)
            lbl.next_to(bg.get_top(), DOWN, buff=0.22)
            text_lines = VGroup(*[
                Line(LEFT * 0.78, RIGHT * 0.78,
                     color=GRAY_C, stroke_width=1.0)
                .move_to(bg.get_center() + UP * (0.24 - j * 0.42))
                for j in range(4)
            ])
            return VGroup(bg, lbl, text_lines)

        doc_A = make_doc_card("Văn bản A", ACADEMIA).shift(LEFT * 3.6 + DOWN * 0.35)
        doc_B = make_doc_card("Văn bản B", INDUSTRY).shift(RIGHT * 3.6 + DOWN * 0.35)

        lm_outer = Circle(radius=0.78, color=HIGHLIGHT, stroke_width=3.0,
                          fill_color="#0f1626", fill_opacity=1)
        lm_inner = Circle(radius=0.54, color=HIGHLIGHT,
                          stroke_width=1.2, fill_opacity=0, stroke_opacity=0.4)
        lm_lbl   = T("LM", 28, HIGHLIGHT, weight=BOLD)
        lm_judge = VGroup(lm_outer, lm_inner, lm_lbl).move_to(DOWN * 0.35)

        arr_A = Arrow(
            LEFT * 2.85 + DOWN * 0.35, LEFT * 0.90 + DOWN * 0.35,
            buff=0, color=ACADEMIA, stroke_width=2.2, tip_length=0.22
        )
        arr_B = Arrow(
            RIGHT * 2.85 + DOWN * 0.35, RIGHT * 0.90 + DOWN * 0.35,
            buff=0, color=INDUSTRY, stroke_width=2.2, tip_length=0.22
        )
        pair_tag = T("So sánh từng cặp", 17, HIGHLIGHT, weight=BOLD)
        pair_tag.next_to(lm_judge, DOWN*1.5)

        with self.voiceover(
            text="Năm ngoái tại hội nghị ICLR, nhóm nghiên cứu của Danqi Chen đã trình bày một "
                 "công trình mang tên 'Curating' với một ý tưởng cốt lõi cực kỳ tinh gọn: sử dụng "
                 "các mô hình ngôn ngữ để đánh giá chất lượng văn bản thông qua phương pháp so sánh "
                 "từng cặp."
        ) as tr:
            self.play(GrowFromCenter(hdr_bg), Write(hdr_txt), run_time=0.85)
            self.wait(0.5)
            self.play(
                FadeIn(doc_A, shift=RIGHT * 0.3),
                FadeIn(doc_B, shift=LEFT  * 0.3),
                run_time=0.65
            )
            self.wait(0.35)
            self.play(GrowArrow(arr_A), GrowArrow(arr_B), run_time=0.6)
            self.play(GrowFromCenter(lm_judge), run_time=0.55)
            self.play(FadeIn(pair_tag, shift=UP * 0.08), run_time=0.45)
            self.wait(max(0, tr.duration - 4.5))

        self.play(FadeOut(VGroup(doc_A, doc_B, arr_A, arr_B, lm_judge, pair_tag)))

        # ═══════════════════════════════════════════════════════════════════════
        # VO2 & VO3 — 4 chiều chất lượng (SỬA LỖI: Dóng trục X độc lập chống lệch cột)
        # ═══════════════════════════════════════════════════════════════════════
        AXES = [
            (ACADEMIA, "1.  Phong cách viết", "Writing Style"),
            (INDUSTRY, "2.  Tính xác thực & truy xuất", "Authenticity & Retrieval"),
            (SUCCESS, "3.  Giá trị giáo dục", "Educational Value"),
            (HIGHLIGHT, "4.  Trình độ chuyên môn", "Required Expertise"),
        ]
        BAR_W, BAR_H = 3.6, 0.40
        SAMPLE_SCORES = [0.78, 0.65, 0.88, 0.72]

        axis_title = T("4 chiều đo chất lượng tài liệu:", 20, WHITE, weight=BOLD)
        axis_title.next_to(header, DOWN, buff=0.48)

        rows = VGroup()
        all_fills = VGroup()
        all_score_labels = VGroup()

        # Thiết lập điểm mốc Y bắt đầu từ UP * 1.0 và hạ dần xuống cho từng hàng
        start_y = 1.0
        row_gap = 0.75

        for idx, ((col, vn, _), score) in enumerate(zip(AXES, SAMPLE_SCORES)):
            current_y = start_y - idx * row_gap

            # 1. Nhãn chữ - Đóng đinh biên trái cố định tại X = -4.5
            lbl = T(vn, 20, col, weight=BOLD)
            lbl.move_to([-4.5, current_y, 0])
            lbl.align_to(np.array([-4.5, current_y, 0]), LEFT)

            # 2. Hộp nền viền - Đóng đinh biên trái cố định tuyệt đối tại X = -1.0
            bg = Rectangle(width=BAR_W, height=BAR_H,
                           fill_color="#111827", fill_opacity=1.0,
                           stroke_color=col, stroke_width=1.4)
            bg.move_to([-0, current_y, 0])
            bg.align_to(np.array([-0, current_y, 0]), LEFT)

            # 3. Năng lượng Fill bên trong (Bám khít theo viền hộp)
            fill = Rectangle(width=BAR_W * score, height=BAR_H,
                             fill_color=col, fill_opacity=0.70, stroke_width=0)
            fill.move_to(bg.get_center())
            fill.align_to(bg, LEFT)

            # 4. Điểm số - Định vị động sát cạnh phải của hộp nền
            score_lbl = T(f"{int(score * 100)}/100", 15, col)
            score_lbl.next_to(bg, RIGHT, buff=0.2)
            score_lbl.align_to(bg, UP)

            # Gom tất cả vào nhóm quản lý hàng
            row = VGroup(lbl, bg, fill, score_lbl)
            rows.add(row)
            all_fills.add(fill)
            all_score_labels.add(score_lbl)

        # Định vị tag chữ kết luận ăn theo lề trái của nhãn chữ hàng đầu tiên
        fp_tag = T("Hồ sơ chất lượng = \"vân tay\" của từng nguồn dữ liệu", 16, NEUTRAL, weight=BOLD)
        fp_tag.move_to([-3, start_y - 4 * row_gap, 0])
        fp_tag.align_to(np.array([-3, 0, 0]), LEFT)

        # Voiceover 1
        with self.voiceover(
                text="Họ định nghĩa chất lượng tài liệu dựa trên 4 trục tọa độ khoa học: phong cách viết, "
                     "tính xác thực và khả năng truy xuất, giá trị giáo dục, và cuối cùng là trình độ "
                     "chuyên môn cần thiết."
        ) as tr:
            self.play(FadeIn(axis_title, shift=DOWN * 0.06), run_time=0.35)
            self.wait(0.2)
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1]), shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15),
                      run_time=1.0)
            self.wait(max(0, tr.duration - 2.5))

        # Voiceover 2
        with self.voiceover(
                text="Khung phân tích này hoạt động hiệu quả đến mức nó trở thành một công cụ mạnh mẽ "
                     "để bóc tách nội dung và hiểu rõ sự trồi sụt chất lượng giữa các miền tri thức khác nhau."
        ) as tr:
            self.play(LaggedStart(*[GrowFromEdge(f, LEFT) for f in all_fills], lag_ratio=0.22), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(sl) for sl in all_score_labels], lag_ratio=0.15), run_time=0.55)
            self.wait(0.5)
            self.play(FadeIn(fp_tag, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0, tr.duration - 3.3))

        self.play(FadeOut(VGroup(axis_title, rows, fp_tag)))

        # ═══════════════════════════════════════════════════════════════════════
        # VO4 — arXiv vs Wikipedia (SỬA LỖI: Chú thích thẳng hàng tuyệt đối theo từng cột)
        # ═══════════════════════════════════════════════════════════════════════
        DIM_NAMES = ["Phong cách", "Xác thực", "Giáo dục", "Chuyên môn"]
        ARXIV_SCORES = [0.72, 0.58, 0.88, 0.93]
        WIKI_SCORES = [0.68, 0.91, 0.76, 0.52]

        CMP_W, CMP_H = 2.0, 0.28
        cmp_title = T("arXiv vs Wikipedia — hồ sơ chất lượng:", 20, WHITE, weight=BOLD)
        cmp_title.next_to(header, DOWN, buff=0.48)

        cmp_rows = VGroup()
        arxiv_fills = VGroup()
        wiki_fills = VGroup()

        # Hệ thống trục X dóng hàng cố định của các cột dữ liệu
        X_LABEL = -4.5  # Trục biên trái nhãn danh mục ("Phong cách", "Xác thực"...)
        X_ARXIV_BAR = -2.2  # Trục biên trái của cột thanh arXiv
        X_WIKI_BAR = 1.0  # Trục biên trái của cột thanh Wikipedia

        start_y_cmp = 1.0
        row_gap_cmp = 0.70

        for idx, (dim, a_s, w_s) in enumerate(zip(DIM_NAMES, ARXIV_SCORES, WIKI_SCORES)):
            current_y = start_y_cmp - idx * row_gap_cmp

            # 1. Nhãn tên chiều danh mục
            dim_lbl = T(dim, 15, GRAY_A, weight=BOLD)
            dim_lbl.move_to([X_LABEL, current_y, 0])
            dim_lbl.align_to(np.array([X_LABEL, current_y, 0]), LEFT)

            # 2. Thanh dữ liệu cột đại diện cho arXiv
            a_bg = Rectangle(width=CMP_W, height=CMP_H,
                             fill_color="#061424", fill_opacity=1,
                             stroke_color=ACADEMIA, stroke_width=0.9)
            a_bg.move_to([X_ARXIV_BAR, current_y, 0])
            a_bg.align_to(np.array([X_ARXIV_BAR, current_y, 0]), LEFT)

            a_fill = Rectangle(width=CMP_W * a_s, height=CMP_H,
                               fill_color=ACADEMIA, fill_opacity=0.75, stroke_width=0)
            a_fill.move_to(a_bg.get_center())
            a_fill.align_to(a_bg, LEFT)

            a_sc = T(str(int(a_s * 100)), 14, ACADEMIA)
            a_sc.next_to(a_bg, RIGHT, buff=0.1)

            # 3. Thanh dữ liệu cột đại diện cho Wikipedia
            w_bg = Rectangle(width=CMP_W, height=CMP_H,
                             fill_color="#191200", fill_opacity=1,
                             stroke_color=HIGHLIGHT, stroke_width=0.9)
            w_bg.move_to([X_WIKI_BAR, current_y, 0])
            w_bg.align_to(np.array([X_WIKI_BAR, current_y, 0]), LEFT)

            w_fill = Rectangle(width=CMP_W * w_s, height=CMP_H,
                               fill_color=HIGHLIGHT, fill_opacity=0.75, stroke_width=0)
            w_fill.move_to(w_bg.get_center())
            w_fill.align_to(w_bg, LEFT)

            w_sc = T(str(int(w_s * 100)), 14, HIGHLIGHT)
            w_sc.next_to(w_bg, RIGHT, buff=0.1)

            # Gom toàn bộ nhóm thành phần một hàng vào Group chính
            row = VGroup(dim_lbl, a_bg, a_fill, a_sc, w_bg, w_fill, w_sc)
            cmp_rows.add(row)
            arxiv_fills.add(a_fill)
            wiki_fills.add(w_fill)

        # ── SỬA ĐỔI CHÚ THÍCH (LEGEND) THẲNG HÀNG VỚI ỨNG CỘT ──
        # Xác định tọa độ Y an toàn nằm phía dưới hàng cuối cùng của bảng dữ liệu
        y_legend = start_y_cmp - 4 * row_gap_cmp

        # Chú thích cột arXiv: Khóa biên trái tại X_ARXIV_BAR (-2.2)
        leg_a = VGroup(Rectangle(width=0.30, height=0.18, fill_color=ACADEMIA, fill_opacity=0.82),
                       T("arXiv", 15, ACADEMIA, weight=BOLD)).arrange(RIGHT, buff=0.1)
        leg_a.move_to([X_ARXIV_BAR, y_legend, 0])
        leg_a.align_to(np.array([X_ARXIV_BAR, 0, 0]), LEFT)

        # Chú thích cột Wikipedia: Khóa biên trái tại X_WIKI_BAR (1.0)
        leg_w = VGroup(Rectangle(width=0.30, height=0.18, fill_color=HIGHLIGHT, fill_opacity=0.82),
                       T("Wikipedia", 15, HIGHLIGHT, weight=BOLD)).arrange(RIGHT, buff=0.1)
        leg_w.move_to([X_WIKI_BAR, y_legend, 0])
        leg_w.align_to(np.array([X_WIKI_BAR, 0, 0]), LEFT)

        # Gom 2 chú thích rời rạc thành 1 khối để quản lý hiệu ứng đồng bộ
        cmp_legend = VGroup(leg_a, leg_w)

        with self.voiceover(
                text="Ví dụ, các bài báo khoa học trên kho lưu trữ arXiv luôn đạt điểm vượt trội về độ "
                     "chuyên môn, trong khi Wikipedia áp đảo về tính xác thực và lượng thông tin cốt lõi."
        ) as tr:
            self.play(FadeIn(cmp_title), run_time=0.4)
            # Khởi hiện kết cấu viền, nhãn và hệ thống chú thích đã dóng trục thẳng tắp
            self.play(
                FadeIn(cmp_legend),
                *[FadeIn(VGroup(r[0], r[1], r[3], r[4], r[6])) for r in cmp_rows],
                run_time=0.7
            )
            self.wait(2.2)

            # Hiệu ứng đổ đầy năng lượng các cột dữ liệu sinh động
            self.play(LaggedStart(*[GrowFromEdge(f, LEFT) for f in arxiv_fills], lag_ratio=0.2), run_time=0.95)
            self.play(Indicate(arxiv_fills[3], color=ACADEMIA, scale_factor=1.06), run_time=0.55)
            self.wait(2)
            self.play(LaggedStart(*[GrowFromEdge(f, LEFT) for f in wiki_fills], lag_ratio=0.2), run_time=0.95)
            self.play(Indicate(wiki_fills[1], color=HIGHLIGHT, scale_factor=1.06), run_time=0.55)

        # ─────────────────────────────────────────────────────────────────────
        # VO5 — Phân hóa nội miền
        # ─────────────────────────────────────────────────────────────────────
        var_lbl = T("Ngay trong cùng một miền: chất lượng vẫn phân hóa rất lớn!", 18, INDUSTRY, weight=BOLD)
        var_line = Line(LEFT * 3.8, RIGHT * 3.8, color=INDUSTRY, stroke_width=2.0)
        var_group = VGroup(var_lbl, var_line).arrange(DOWN, buff=0.15)
        var_group.move_to(DOWN * 3)

        with self.voiceover(
                text="Tuy nhiên, chất lượng tài liệu ngay trong từng miền vẫn có sự phân hóa rất lớn."
        ) as tr:
            self.play(FadeIn(var_lbl, shift=DOWN * 0.10), Create(var_line), run_time=0.65)
            self.wait(max(0, tr.duration - 0.85))

        self.play(FadeOut(VGroup(cmp_title, cmp_rows, arxiv_fills, wiki_fills, cmp_legend, var_group)))

        # ─────────────────────────────────────────────────────────────────────
        # VO6 — Common Crawl Challenge (căn lề trái danh sách)
        # ─────────────────────────────────────────────────────────────────────
        cc_title = T("Nhưng làm thế nào với Common Crawl — không có cấu trúc?", 19, WHITE, weight=BOLD)
        cc_title.next_to(header, DOWN, buff=0.48)

        # Phần trái: có cấu trúc
        struct_bg = RoundedRectangle(corner_radius=0.14, width=3.2, height=2.7,
                                     fill_color="#061828", fill_opacity=1.0,
                                     stroke_color=SUCCESS, stroke_width=2.0)
        struct_bg.move_to(LEFT * 2.8 + DOWN * 0.6)

        struct_head = T("Có cấu trúc", 17, SUCCESS, weight=BOLD)
        struct_head.next_to(struct_bg.get_top(), DOWN, buff=0.22)

        src_list = ["Wikipedia", "arXiv", "Books3"]
        items_group = VGroup()
        for name in src_list:
            ok = T("[+]", 15, SUCCESS, weight=BOLD)
            item = T(name, 16, GRAY_A)
            row = VGroup(ok, item).arrange(RIGHT, buff=0.14)
            items_group.add(row)
        items_group.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        # Đặt bên trong khung, căn lề trái
        items_group.move_to(struct_bg.get_center() + DOWN * 0.1)
        items_group.align_to(struct_bg.get_left() + RIGHT * 0.3, LEFT)

        vs_t = T("VS", 22, NEUTRAL, weight=BOLD).move_to(DOWN * 0.6)

        # Phần phải: Common Crawl hỗn loạn
        cc_bg = RoundedRectangle(corner_radius=0.14, width=3.2, height=2.7,
                                 fill_color="#1a0505", fill_opacity=1.0,
                                 stroke_color=INDUSTRY, stroke_width=2.0)
        cc_bg.move_to(RIGHT * 2.8 + DOWN * 0.6)

        cc_head = T("Common Crawl", 17, INDUSTRY, weight=BOLD)
        cc_head.next_to(cc_bg.get_top(), DOWN, buff=0.22)

        rng = np.random.default_rng(seed=42)
        _dot_cols = [INDUSTRY, GRAY_C, NEUTRAL, GRAY_B, INDUSTRY]
        chaos_dots = VGroup(*[
            Dot(point=RIGHT * 2.8 + DOWN * 0.6 + np.array([rng.uniform(-1.1, 1.1), rng.uniform(-0.95, 0.65), 0.0]),
                radius=0.065, color=_dot_cols[j % len(_dot_cols)])
            for j in range(28)
        ])

        big_q = T("?", 72, HIGHLIGHT, weight=BOLD).move_to(DOWN * 0.6)

        with self.voiceover(
                text="Điều này đặt ra một dấu hỏi lớn hơn: Chúng ta có thể phân tích được các miền có "
                     "cấu trúc như Wiki hay arXiv, nhưng làm thế nào để xử lý và hiểu được đại dương "
                     "dữ liệu web khổng lồ không có cấu trúc như Common Crawl?"
        ) as tr:
            self.play(FadeIn(cc_title, shift=DOWN * 0.07), run_time=0.5)
            self.wait(0.3)
            self.play(FadeIn(struct_bg), Write(struct_head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.1) for row in items_group], lag_ratio=0.22),
                      run_time=0.8)
            self.wait(2)
            self.play(GrowFromCenter(vs_t), run_time=0.3)
            self.play(FadeIn(cc_bg), Write(cc_head), run_time=0.5)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in chaos_dots], lag_ratio=0.06), run_time=0.95)
            self.wait(0.5)
            self.play(FadeOut(VGroup(struct_bg, struct_head, items_group, cc_bg, cc_head, chaos_dots, vs_t)),
                      run_time=0.4)
            self.play(GrowFromCenter(big_q), run_time=0.55)
            flash_mob(self, big_q, color=HIGHLIGHT, radius=1.0)
            self.wait(max(0, tr.duration - 5.85))

        self.wait(0.5)
        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — P4_WebOrganizer
# ══════════════════════════════════════════════════════════════════════════════
class P4_WebOrganizer(VoiceoverScene):
    def construct(self):
        # Khởi tạo dịch vụ voice-over (Google Text-to-Speech)
        self.set_speech_service(svc())

        # ── Header ───────────────────────────────────────────
        hdr_bg = RoundedRectangle(corner_radius=0.15, width=7.5, height=0.85,
                                  color=HIGHLIGHT, fill_color=HIGHLIGHT,
                                  fill_opacity=0.10, stroke_width=1.5)
        hdr_txt = title_card("WebOrganizer  &  RegMix", HIGHLIGHT, size=27)
        header = VGroup(hdr_bg, hdr_txt).shift(UP * 2.7)

        with self.voiceover(
                text="Để giải bài toán hóc búa đó, năm nay họ đã dồn lực vào dự án WebOrganizer — "
                     "một công trình hợp tác cùng các công cụ AI nhưng vận hành hoàn toàn trong một "
                     "ngân sách học thuật khiêm tốn của phòng lab trường đại học."
        ) as tr:
            self.play(GrowFromCenter(hdr_bg), Write(hdr_txt), run_time=1.2)
            self.wait(max(0, tr.duration - 1.3))

        # ── 3.2 Topic × Format 2D grid ─────────────────────────
        concept_t = T("WebOrganizer: Biến web hỗn loạn thành dữ liệu có cấu trúc", 20, WHITE)
        concept_t.next_to(header, DOWN, buff=0.4)

        pages = VGroup(*[
            RoundedRectangle(width=0.9, height=0.4, corner_radius=0.05,
                             fill_color=GRAY, fill_opacity=0.2,
                             stroke_color=GRAY_B, stroke_width=1)
            for _ in range(24)
        ])
        pages.arrange_in_grid(rows=4, cols=6, buff=0.1)
        pages.move_to(DOWN * 0.4)

        web_box = SurroundingRectangle(pages, color=HIGHLIGHT, corner_radius=0.15)
        web_label = T("Web hỗn hợp", 18, HIGHLIGHT, weight="BOLD")
        web_label.next_to(web_box, UP)

        with self.voiceover(
                text="Kết quả thu được vô cùng ấn tượng. WebOrganizer đã phân tách thành công lượng dữ liệu web hỗn mạt thành các miền tri thức có cấu trúc hai chiều cực kỳ dễ hiểu, thông qua hai hệ thống phân loại bổ sung cho nhau là chủ đề và định dạng."
        ) as tr:
            self.play(FadeIn(concept_t))
            dirs = [UP, DOWN, LEFT, RIGHT, UP + LEFT, UP + RIGHT]
            self.play(LaggedStart(*[FadeIn(p, shift=dirs[i % len(dirs)] * 0.25) for i, p in enumerate(pages)],
                                  lag_ratio=0.08))
            self.play(Create(web_box), FadeIn(web_label))
            self.wait(0.5)
            self.wait(max(0, tr.duration - 2.3))

        # ---------------------------------------------------------
        # CHUYỂN SANG TOPIC + FORMAT (có màu sắc, tránh đè viền)
        # ---------------------------------------------------------
        self.play(FadeOut(concept_t), FadeOut(web_box), FadeOut(web_label))

        # Panel lớn hơn một chút và có fill màu nhẹ
        topic_panel = RoundedRectangle(width=3.6, height=2.3, corner_radius=0.15,
                                       stroke_color=ACADEMIA, fill_color=ACADEMIA, fill_opacity=0.05)
        topic_panel.move_to(LEFT * 3.2)
        topic_title = T("Topic", 22, ACADEMIA, weight="BOLD")
        topic_title.next_to(topic_panel, UP, buff=0.15)

        format_panel = RoundedRectangle(width=3.6, height=2.3, corner_radius=0.15,
                                        stroke_color=SUCCESS, fill_color=SUCCESS, fill_opacity=0.05)
        format_panel.move_to(RIGHT * 3.2)
        format_title = T("Format", 22, SUCCESS, weight="BOLD")
        format_title.next_to(format_panel, UP, buff=0.15)

        self.play(Create(topic_panel), Create(format_panel), FadeIn(topic_title), FadeIn(format_title))

        # Chia 24 ô thành 2 nhóm, mỗi nhóm 12 ô
        left_pages = pages[:12]
        right_pages = pages[12:]

        # Tạo lưới con 3x4, điều chỉnh kích thước ô nhỏ hơn để vừa panel
        grid_topic = VGroup(*left_pages).copy()
        for rect in grid_topic:
            rect.set(width=0.85, height=0.38)
        grid_topic.arrange_in_grid(rows=4, cols=3, buff=0.08)
        grid_topic.move_to(topic_panel.get_center())

        grid_format = VGroup(*right_pages).copy()
        for rect in grid_format:
            rect.set(width=0.85, height=0.38)
        grid_format.arrange_in_grid(rows=4, cols=3, buff=0.08)
        grid_format.move_to(format_panel.get_center())

        # Thay đổi màu sắc các ô (topic: xanh dương nhạt, format: xanh ngọc nhạt)
        for rect in grid_topic:
            rect.set_fill(ACADEMIA, opacity=0.3)
            rect.set_stroke(ACADEMIA, width=1.5)
        for rect in grid_format:
            rect.set_fill(SUCCESS, opacity=0.3)
            rect.set_stroke(SUCCESS, width=1.5)

        self.play(
            *[ReplacementTransform(left_pages[i], grid_topic[i]) for i in range(12)],
            *[ReplacementTransform(right_pages[i], grid_format[i]) for i in range(12)],
            run_time=1.5
        )

        desc = T("Mỗi trang web được gán đồng thời một chủ đề và định dạng", 16, WHITE)
        desc.next_to(VGroup(topic_panel, format_panel), DOWN, buff=0.5)

        with self.voiceover(
                text="Mỗi trang web giờ đây không còn là một phần tử vô danh, mà được gắn đồng thời vào một chủ đề và định dạng cụ thể."
        ) as tr:
            self.play(FadeIn(desc))

        self.play(FadeOut(VGroup(topic_panel, format_panel, topic_title, format_title, grid_topic, grid_format, desc)))

        # ── FORMAT SKEW ─────────────────────────────────────
        skew_title = T("Phân phối định dạng bị thiên lệch mạnh", 22, INDUSTRY, weight=BOLD)
        skew_title.next_to(header, DOWN, buff=0.4)

        bars_data = [("Blog", 48, INDUSTRY), ("Quảng cáo", 22, INDUSTRY),
                     ("Tin tức", 12, ACADEMIA), ("Giáo dục", 9, SUCCESS),
                     ("Học thuật", 5, HIGHLIGHT)]
        bars = VGroup()
        for name, val, col in bars_data:
            bar = Rectangle(width=0.9, height=val * 0.06, fill_color=col, fill_opacity=0.7, stroke_color=col)
            pct = T(f"{val}%", 12, col, weight=BOLD)
            lbl = T(name, 12, WHITE)
            grp = VGroup(bar, pct, lbl)
            pct.next_to(bar, UP, buff=0.05)
            lbl.next_to(bar, DOWN, buff=0.1)
            bars.add(grp)
        bars.arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        bars.move_to(DOWN * 0.5)

        with self.voiceover(
                text="Hình ảnh trực quan hóa từ WebOrganizer phơi bày một thực tế. Trong khi các chủ đề trên web phân bổ tương đối đồng đều, thì định dạng lại bị thiên lệch nghiêm trọng, với phần lớn dữ liệu đến từ blog cá nhân và các trang quảng cáo."
        ) as tr:
            self.play(FadeIn(skew_title))
            for g in bars:
                self.play(GrowFromEdge(g[0], DOWN), run_time=0.3)
                self.play(FadeIn(g[1]), FadeIn(g[2]), run_time=0.15)
            flash_mob(self, bars[0][0], INDUSTRY, 0.6)
            flash_mob(self, bars[1][0], INDUSTRY, 0.6)
            self.wait(max(0, tr.duration - 3.0))

        # ── QUESTION ────────────────────────────────────────
        question = T("Làm sao phối trộn các miền dữ liệu?", 33, HIGHLIGHT, weight=BOLD)
        question.move_to(DOWN * 0.5)
        with self.voiceover(
                text="Vậy làm thế nào để biến những phân vùng dữ liệu này thành một tập dữ liệu huấn luyện vượt trội?"
        ) as tr:
            self.play(bars.animate.set_opacity(0.4))
            self.play(skew_title.animate.set_opacity(0.4))
            self.play(FadeIn(question))
            self.wait(max(0, tr.duration - 1.2))
        self.play(FadeOut(question), FadeOut(skew_title), FadeOut(bars))

        # ── 3.5 RegMix framework ─────────────────────────────────────

        regmix_title = T(
            "RegMix: Tìm tỷ lệ pha trộn dữ liệu tối ưu",
            22,
            WHITE,
            weight=BOLD
        )

        regmix_title.next_to(header, DOWN, buff=0.35)

        # =====================================================
        # Domain sources
        # =====================================================

        domain_names = [
            ("Blog", INDUSTRY),
            ("Tin tức", HIGHLIGHT),
            ("Khoa học", SUCCESS),
            ("Giáo dục", ACADEMIA),
        ]

        domains = VGroup()

        for name, col in domain_names:
            box = RoundedRectangle(
                width=1.6,
                height=0.6,
                corner_radius=0.1,
                fill_color=col,
                fill_opacity=0.15,
                stroke_color=col,
            )

            txt = T(name, 15, col, weight=BOLD)

            domains.add(
                VGroup(box, txt)
            )

        domains.arrange(RIGHT, buff=0.35)
        domains.move_to(UP * 0.9)

        # =====================================================
        # Mix layer
        # =====================================================

        mix_box = RoundedRectangle(
            width=3.2,
            height=0.8,
            corner_radius=0.12,
            fill_color=HIGHLIGHT,
            fill_opacity=0.15,
            stroke_color=HIGHLIGHT,
        )

        mix_text = T(
            "Mix",
            16,
            HIGHLIGHT,
            weight=BOLD
        )

        mix_layer = VGroup(
            mix_box,
            mix_text
        )

        mix_layer.move_to(ORIGIN)

        # arrows

        mix_arrows = VGroup()

        for d in domains:
            mix_arrows.add(
                Arrow(
                    d.get_bottom(),
                    mix_layer.get_top(),
                    stroke_width=2,
                    buff=0.12,
                    color=d[0].get_stroke_color(),
                    tip_length=0.1
                )
            )

        # =====================================================
        # Proxy model
        # =====================================================

        proxy_box = RoundedRectangle(
            width=3.8,
            height=0.9,
            corner_radius=0.12,
            fill_color=SUCCESS,
            fill_opacity=0.12,
            stroke_color=SUCCESS
        )

        proxy_text = VGroup(
            T("Proxy Models", 16, SUCCESS, weight=BOLD),
            T("50M params × 1B token", 13, GRAY_A)
        ).arrange(DOWN, buff=0.08)

        proxy_layer = VGroup(
            proxy_box,
            proxy_text
        )

        proxy_layer.move_to(DOWN * 1.4)

        arrow_proxy = Arrow(
            mix_layer.get_bottom(),
            proxy_layer.get_top(),
            buff=0.12,
            color=SUCCESS
        )

        with self.voiceover(
                text=
                "Ý tưởng của RegMix là tạo ra hàng trăm hỗn hợp dữ liệu khác nhau. "
                "Mỗi hỗn hợp sau đó được dùng để huấn luyện một mô hình proxy rất nhỏ, "
                "chỉ khoảng năm mươi triệu tham số trên một tỷ token."
        ) as tr:

            self.play(FadeIn(regmix_title))

            self.play(
                LaggedStart(
                    *[GrowFromCenter(d) for d in domains],
                    lag_ratio=0.15
                )
            )

            self.play(
                LaggedStart(
                    *[GrowArrow(a) for a in mix_arrows],
                    lag_ratio=0.08
                )
            )

            self.play(
                GrowFromCenter(mix_layer)
            )

            self.play(
                GrowArrow(arrow_proxy),
                GrowFromCenter(proxy_layer)
            )

            self.wait(max(0, tr.duration - 3.5))

            regmix_visuals = VGroup(
                domains,
                mix_arrows,
                mix_layer,
                arrow_proxy,
                proxy_layer,
            )

            self.play(
                FadeOut(
                    regmix_visuals,
                    shift=DOWN * 0.2
                ),
                run_time=0.7
            )

        # ── 3.6 Regression ───────────────────────────────────

        reg_title = T(
            "Dự đoán hiệu suất bằng hồi quy",
            21,
            SUCCESS,
            weight=BOLD
        )

        reg_title.next_to(header, DOWN, buff=0.35)

        self.play(
            Transform(regmix_title, reg_title)
        )

        # scatter area

        plot_box = Rectangle(
            width=6,
            height=3.5,
            color=GRAY_B
        )

        plot_box.move_to(DOWN * 0.4)

        rng = np.random.default_rng(42)

        proxy_dots = VGroup()

        for _ in range(30):
            x = rng.uniform(-2.5, 2.5)
            y = 0.55 * x + rng.normal(scale=0.45)

            dot = Dot(
                radius=0.05,
                color=GRAY_B
            )

            dot.move_to(
                plot_box.get_center()
                + RIGHT * x
                + UP * y
            )

            proxy_dots.add(dot)

        reg_line = Line(
            plot_box.get_left() + RIGHT * 0.5 + DOWN * 0.8,
            plot_box.get_right() + LEFT * 0.5 + UP * 0.8,
            color=SUCCESS,
            stroke_width=3
        )

        best_dot = Dot(
            radius=0.12,
            color=HIGHLIGHT
        )

        best_dot.move_to(
            reg_line.point_from_proportion(0.88)
        )

        best_ring = Circle(
            radius=0.25,
            color=HIGHLIGHT
        )

        best_ring.move_to(best_dot)

        best_label = T(
            "Mix tốt nhất",
            15,
            HIGHLIGHT,
            weight=BOLD
        )

        best_label.next_to(best_ring, RIGHT)

        with self.voiceover(
                text=
                "Từ kết quả của các mô hình proxy này, RegMix xây dựng một mô hình hồi quy "
                "để dự đoán hiệu suất của những tỷ lệ pha trộn khác nhau, sau đó xác định "
                "cấu hình dữ liệu triển vọng nhất."
        ) as tr:

            self.play(Create(plot_box))

            self.play(
                LaggedStart(
                    *[FadeIn(d, scale=0.5) for d in proxy_dots],
                    lag_ratio=0.03
                ),
                run_time=1
            )

            self.play(
                Create(reg_line),
                run_time=0.8
            )

            self.play(
                GrowFromCenter(best_dot),
                Create(best_ring)
            )

            self.play(
                FadeIn(best_label)
            )

            self.wait(max(0, tr.duration - 2.8))
            clear(self)

class P4_RegmixResults(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        hdr_bg  = RoundedRectangle(corner_radius=0.15, width=7.5, height=0.85,
                                    color=SUCCESS, fill_color=SUCCESS,
                                    fill_opacity=0.10, stroke_width=1.5)
        hdr_txt = title_card("Kết quả RegMix — Tác động thực tế", SUCCESS, size=26)
        header  = VGroup(hdr_bg, hdr_txt).shift(UP * 2.7)

        with self.voiceover(
            text="Tác động của việc tối ưu hóa kết hợp miền này là một cú hích thực sự lớn."
        ) as tr:
            self.play(GrowFromCenter(hdr_bg), Write(hdr_txt), run_time=1.0)
            self.wait(max(0, tr.duration - 1.1))

        # ── 4.1 Baseline: 51.6 ────────────────────────────────────────────────
        chart_title = T("Điểm trung bình trên 9 tác vụ hạ nguồn (1B / 29B token):", 18, WHITE)
        chart_title.next_to(header, DOWN, buff=0.4)
        self.play(FadeIn(chart_title))

        bar_data = [
            ("Uniform\nSampling\n", 51.6, NEUTRAL),
            ("Topic\nMixture",                53.7, ACADEMIA),
            ("Format\nMixture",               53.4, INDUSTRY),
            ("Topic\nFormat",               54.6, HIGHLIGHT),
            ("RegMix\nQuality",             56.2, SUCCESS),
        ]
        base_y    = DOWN * 2.0
        bar_width = 1.0
        bar_gap   = 0.35
        total_w   = len(bar_data) * (bar_width + bar_gap) - bar_gap
        x_start   = -total_w / 2 + bar_width / 2
        score_min = 50.5
        score_max = 57.0
        chart_h   = 3.0
        scale     = chart_h / (score_max - score_min)

        base_h    = (51.6 - score_min) * scale
        base_line = DashedLine(
            [x_start - bar_width * 0.6, -2.0 + base_h, 0],
            [x_start + total_w + bar_width * 0.1, -2.0 + base_h, 0],
            color=NEUTRAL, stroke_width=1.2, dash_length=0.12
        )

        with self.voiceover(
            text="Trên cùng một quy mô mô hình 1B với 29 tỷ token, việc chỉ lấy mẫu đồng đều "
                 "(Uniform sampling) từ Common Crawl chỉ mang lại kết quả trung bình thấp."
        ) as tr:
            self.play(Create(base_line), run_time=0.6)
            nm, score, col = bar_data[0]
            bar_h  = (score - score_min) * scale
            x_pos  = x_start + 0 * (bar_width + bar_gap)
            bar0   = Rectangle(width=bar_width, height=bar_h,
                                fill_color=col, fill_opacity=0.75,
                                stroke_color=col, stroke_width=1.5)
            bar0.align_to(base_y, DOWN).shift(RIGHT * x_pos)
            sc0 = T(f"{score}", 14, col, weight=BOLD).next_to(bar0, UP, buff=0.07)
            lb0 = T(nm, 11, WHITE).next_to(bar0, DOWN, buff=0.1)
            self.play(GrowFromEdge(bar0, DOWN), FadeIn(sc0), FadeIn(lb0), run_time=0.8)
            self.wait(max(0, tr.duration - 1.8))

        with self.voiceover(
            text="Nhưng khi kết hợp tối ưu cả chủ đề lẫn định dạng theo thuật toán Regmix, hiệu "
                 "suất trung bình trên 9 tác vụ hạ nguồn đã lập tức nhảy vọt từ 51,6 lên 56,2."
        ) as tr:
            bar_grps = [VGroup(bar0, sc0, lb0)]
            for idx in range(1, 4):
                nm, score, col = bar_data[idx]
                bar_h  = (score - score_min) * scale
                x_pos  = x_start + idx * (bar_width + bar_gap)
                br = Rectangle(width=bar_width, height=bar_h,
                               fill_color=col, fill_opacity=0.75,
                               stroke_color=col, stroke_width=1.5)
                br.align_to(base_y, DOWN).shift(RIGHT * x_pos)
                sc = T(f"{score}", 14, col, weight=BOLD).next_to(br, UP, buff=0.07)
                lb = T(nm, 11, WHITE).next_to(br, DOWN, buff=0.1)
                self.play(GrowFromEdge(br, DOWN), FadeIn(sc), FadeIn(lb), run_time=0.55)
                bar_grps.append(VGroup(br, sc, lb))
            # Final bar (RegMix + Quality)
            nm, score, col = bar_data[4]
            bar_h  = (score - score_min) * scale
            x_pos  = x_start + 4 * (bar_width + bar_gap)
            br5 = Rectangle(width=bar_width, height=bar_h,
                             fill_color=col, fill_opacity=0.88,
                             stroke_color=col, stroke_width=2.5)
            br5.align_to(base_y, DOWN).shift(RIGHT * x_pos)
            sc5 = T(f"{score}", 17, col, weight=BOLD).next_to(br5, UP, buff=0.07)
            lb5 = T(nm, 11, WHITE).next_to(br5, DOWN, buff=0.1)
            self.play(GrowFromEdge(br5, DOWN), FadeIn(sc5), FadeIn(lb5), run_time=0.9)
            flash_mob(self, br5, color=SUCCESS, radius=0.7)
            bar_grps.append(VGroup(br5, sc5, lb5))
            delta_t = T("+4.6 vs baseline", 14, SUCCESS, weight=BOLD)
            delta_t.next_to(sc5, RIGHT, buff=0.2)
            self.play(FadeIn(delta_t, shift=LEFT * 0.15), run_time=0.5)
            self.wait(max(0, tr.duration - 4.0))

        # ── 4.2 Matches FineWeb-edu ───────────────────────────────────────────
        fw_lbl = T("≈ FineWeb-edu của Hugging Face (đình đám toàn cầu)", 16, HIGHLIGHT, weight=BOLD)
        fw_lbl.next_to(lb5, DOWN, buff=0.25)

        with self.voiceover(
            text="Mức tăng trưởng ngoạn mục này hoàn toàn sánh ngang với bộ lọc FineWeb-edu "
                 "đình đám của Hugging Face."
        ) as tr:
            self.play(FadeIn(fw_lbl, shift=UP * 0.1), run_time=0.5)
            flash_mob(self, fw_lbl, color=HIGHLIGHT, radius=1.3)
            self.wait(max(0, tr.duration - 1.0))

        with self.voiceover(
            text="Nó chứng minh một sự thật: các hỗn hợp miền tối ưu đã chủ động lựa chọn nhiều "
                 "hơn các tài liệu khoa học công nghệ, các bài viết học thuật hướng dẫn và gạt bỏ "
                 "các nội dung rác."
        ) as tr:
            pref_t = T("Optimal mix → ưu tiên: Khoa học, Học thuật   |  loại bỏ: Rác ",
                        15, SUCCESS)
            pref_t.next_to(fw_lbl, DOWN, buff=0.22)
            self.play(FadeIn(pref_t, shift=UP * 0.08), run_time=0.6)
            self.wait(max(0, tr.duration - 0.9))

        self.play(FadeOut(VGroup(chart_title, base_line, delta_t,
                                  fw_lbl, pref_t,
                                  *bar_grps)))
        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 5 — P4_Prolong
# ══════════════════════════════════════════════════════════════════════════════
class P4_Prolong(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ---------------------------------------------------------
        # Layout anchors
        # ---------------------------------------------------------
        TOP_Y = 2.7

        hdr_bg = RoundedRectangle(
            corner_radius=0.2,
            width=7.8,
            height=1.0,
            color=ACADEMIA,
            fill_color=ACADEMIA,
            fill_opacity=0.12,
            stroke_width=2,
        )

        hdr_txt = title_card("DỰ ÁN: ProLong", size=30)

        header = VGroup(hdr_bg, hdr_txt)
        header.move_to(UP * TOP_Y)

        # =========================================================
        # 5.1 Goal: 8B / 512K
        # =========================================================
        with self.voiceover(
            text="Để chứng minh sức mạnh của dữ liệu, dự án PROLONG được thực hiện với ngân"
                 "sách gấp 10 lần cho mục tiêu là xây dựng một mô hình 8 tỷ tham số hỗ trợ "
                 " độ dài ngữ cảnh không tưởng lên đến 512K."
        ) as tr:

            self.play(
                GrowFromCenter(hdr_bg),
                Write(hdr_txt),
                run_time=1.0,
            )

            goal_t = T(
                "8B params  ·  ngữ cảnh 512K tokens",
                21,
                HIGHLIGHT,
                weight=BOLD,
            )

            goal_t.next_to(header, DOWN, buff=0.45)

            self.play(
                FadeIn(goal_t, shift=DOWN * 0.1),
                run_time=0.6,
            )

            self.wait(max(0, tr.duration - 1.8))

        # =========================================================
        # 5.2 Start: Llama 3 8B (8K)
        # =========================================================
        start_t = T(
            "Điểm xuất phát: Llama 3 8B (8K context)",
            19,
            WHITE,
        )

        start_t.next_to(goal_t, DOWN, buff=0.35)

        bar_bg = Rectangle(
            width=7.2,
            height=0.58,
            fill_color=GRAY_D,
            fill_opacity=0.35,
            stroke_color=GRAY_C,
            stroke_width=1.0,
        )

        bar_bg.move_to(DOWN * 0.5)

        frac_8k = 8 / 512
        init_w = 7.2 * frac_8k

        bar_init = Rectangle(
            width=max(init_w, 0.14),
            height=0.58,
            fill_color=ACADEMIA,
            fill_opacity=0.85,
            stroke_width=0,
        )

        bar_init.move_to(
            bar_bg.get_left()
            + RIGHT * (bar_init.width / 2)
        )

        bar_init.set_y(bar_bg.get_y())

        lbl_8k = T(
            "8K\n(Llama-3)",
            12,
            ACADEMIA,
        )

        lbl_8k.next_to(bar_init, UP, buff=0.16)

        lbl_512k = T(
            "512K\n(ProLong)",
            12,
            HIGHLIGHT,
        )

        lbl_512k.next_to(bar_bg, RIGHT, buff=0.25)

        tick_0 = T("0", 10, GRAY_B)
        tick_mid = T("256K", 10, GRAY_B)
        tick_end = T("512K", 10, GRAY_B)

        tick_0.move_to(bar_bg.get_left() + DOWN * 0.38)
        tick_mid.move_to(bar_bg.get_center() + DOWN * 0.38)
        tick_end.move_to(bar_bg.get_right() + DOWN * 0.38)

        with self.voiceover(
            text="Vì không thể huấn luyện từ đầu, nhóm nghiên cứu bắt đầu từ mô hình Llama 3 8B "
                 "nguyên bản vốn chỉ hỗ trợ ngữ cảnh 8K."
        ) as tr:

            self.play(FadeIn(start_t), run_time=0.5)

            self.play(
                Create(bar_bg),
                FadeIn(tick_0),
                FadeIn(tick_mid),
                FadeIn(tick_end),
                run_time=0.6,
            )

            self.play(
                GrowFromEdge(bar_init, LEFT),
                run_time=0.7,
            )

            self.play(
                FadeIn(lbl_8k, shift=DOWN * 0.1),
                run_time=0.4,
            )

            self.wait(max(0, tr.duration - 2.4))

        # =========================================================
        # 5.3 40B tokens → 512K
        # =========================================================
        token_lbl = T(
            "Huấn luyện với 40B Tokens",
            17,
            SUCCESS,
            weight=BOLD,
        )

        token_lbl.move_to(DOWN * 1.5)

        with self.voiceover(
            text="Họ đã tiến hành huấn luyện tiếp tục trên 40 tỷ token để kéo giãn cửa sổ ngữ "
                 "cảnh lên mốc 512K."
        ) as tr:

            self.play(
                FadeIn(token_lbl, shift=UP * 0.1),
                run_time=0.5,
            )

            self.play(
                bar_init.animate
                    .stretch_to_fit_width(bar_bg.width)
                    .align_to(bar_bg, LEFT)
                    .set_y(bar_bg.get_y()),
                FadeOut(lbl_8k),
                FadeIn(lbl_512k),
                run_time=2.2,
                rate_func=rush_from,
            )

            flash_mob(
                self,
                lbl_512k,
                color=HIGHLIGHT,
                radius=0.75,
            )

            self.wait(max(0, tr.duration - 3.0))

        self.play(
            FadeOut(
                VGroup(
                    goal_t,
                    start_t,
                    bar_bg,
                    bar_init,
                    lbl_512k,
                    tick_0,
                    tick_mid,
                    tick_end,
                    token_lbl,
                )
            ),
            run_time=0.4,
        )

        # =========================================================
        # 5.4 Meta comparison: 800B vs 40B
        # =========================================================
        eff_title = T(
            "So sánh tài nguyên: ProLong vs Meta Llama-3.1",
            20,
            WHITE,
        )

        eff_title.next_to(header, DOWN, buff=0.45)

        meta_circ = Circle(
            radius=1.5,
            fill_color=INDUSTRY,
            fill_opacity=0.15,
            stroke_color=INDUSTRY,
            stroke_width=2.5,
        )

        meta_circ.move_to(RIGHT * 2.8 + DOWN * 0.20)

        meta_l1 = T(
            "Meta Llama-3.1",
            18,
            INDUSTRY,
            weight=BOLD,
        )

        meta_l2 = T(
            "800B tokens",
            24,
            INDUSTRY,
            weight=SEMIBOLD,
        )

        meta_l1.move_to(meta_circ.get_center() + UP * 0.38)
        meta_l2.move_to(meta_circ.get_center() + DOWN * 0.20)

        prolong_circ = Circle(
            radius=0.65,
            fill_color=ACADEMIA,
            fill_opacity=0.42,
            stroke_color=ACADEMIA,
            stroke_width=2.5,
        )

        prolong_circ.move_to(LEFT * 2.8 + DOWN * 0.20)

        pl1 = T(
            "ProLong",
            14,
            ACADEMIA,
            weight=BOLD,
        )

        pl2 = T(
            "40B tokens",
            12,
            ACADEMIA,
            weight=SEMIBOLD,
        )

        pl1.move_to(prolong_circ.get_center() + UP * 0.18)
        pl2.move_to(prolong_circ.get_center() + DOWN * 0.20)
        with self.voiceover(
            text="Ngay khi hoàn thành, Meta tung ra Llama 3.1 và họ đã phải dùng tới 800 tỷ token "
                 "cho việc huấn luyện ngữ cảnh dài."
        ) as tr:

            self.play(FadeIn(eff_title))

            self.play(
                GrowFromCenter(meta_circ),
                FadeIn(meta_l1),
                FadeIn(meta_l2),
                run_time=0.8,
            )

            self.wait(max(0, tr.duration - 1.2))

        pct_arrow = Arrow(
            prolong_circ.get_right(),
            meta_circ.get_left(),
            buff=0.15,
            color=HIGHLIGHT,
            stroke_width=2.5,
        )

        pct_lbl = T(
            "= 5% tài nguyên Meta!",
            18,
            HIGHLIGHT,
            weight=BOLD,
        )

        pct_lbl.move_to(DOWN * 1.85)

        with self.voiceover(
            text="Nghĩa là, PROLONG chỉ sử dụng vẻn vẹn 5% tài nguyên tính toán của Meta."
        ) as tr:

            self.play(
                GrowFromCenter(prolong_circ),
                FadeIn(pl1),
                FadeIn(pl2),
                run_time=0.6,
            )

            self.play(
                GrowArrow(pct_arrow),
                run_time=0.5,
            )

            self.play(
                FadeIn(pct_lbl, shift=UP * 0.2),
                run_time=0.5,
            )

            flash_mob(
                self,
                pct_lbl,
                color=HIGHLIGHT,
                radius=1.1,
            )

            self.wait(max(0, tr.duration - 2.0))

        # =========================================================
        # 5.5 Performance results
        # =========================================================
        result_rows = VGroup()

        rows_data = [
            (
                "ProLong 8B  ≈  Llama-3.1 8B",
                "Bài đánh giá ngữ cảnh dài",
                ACADEMIA,
                True,
            ),
            (
                "ProLong 8B  >  mọi mô hình <10B",
                "Open-source leaderboard",
                SUCCESS,
                True,
            ),
        ]

        for model, result, col, hl in rows_data:

            rb = RoundedRectangle(
                corner_radius=0.08,
                width=7.0,
                height=0.50,
                fill_color=col,
                fill_opacity=0.20,
                stroke_color=col,
                stroke_width=1.8,
            )

            mt = T(model, 15, col)
            rt = T(result, 14, WHITE)

            mt.move_to([-1.8, 0, 0])
            rt.move_to([2.0, 0, 0])

            result_rows.add(
                VGroup(rb, mt, rt)
            )

        result_rows.arrange(
            DOWN,
            buff=0.18,
            aligned_edge=LEFT,
        )

        result_rows.move_to(DOWN * 3)

        with self.voiceover(
            text="Nhưng khi đưa lên bàn cân đối chiếu, PROLONG vẫn đạt hiệu suất tương đương với "
                 "Llama 3.1 trong các bài đánh giá ngữ cảnh dài, đồng thời vượt trội hơn hầu hết "
                 "các mô hình mã nguồn mở khác dưới 10B tham số trên thị trường."
        ) as tr:

            self.play(
                LaggedStart(
                    *[
                        FadeIn(
                            r,
                            shift=RIGHT * 0.15,
                        )
                        for r in result_rows
                    ],
                    lag_ratio=0.3,
                ),
                run_time=min(
                    1.4,
                    tr.duration * 0.5,
                ),
            )

            flash_mob(
                self,
                result_rows[0],
                color=ACADEMIA,
                radius=0.8,
            )

            flash_mob(
                self,
                result_rows[1],
                color=SUCCESS,
                radius=0.8,
            )

            self.wait(max(0, tr.duration - 3.0))

        self.play(
            FadeOut(
                VGroup(
                    eff_title,
                    meta_circ,
                    meta_l1,
                    meta_l2,
                    prolong_circ,
                    pl1,
                    pl2,
                    pct_arrow,
                    pct_lbl,
                    result_rows,
                )
            ),
            run_time=0.4,
        )

        # =========================================================
        # 5.6 Key = Data
        # =========================================================
        key_t = T(
            "Khẳng định tầm quan trọng của",
            20,
            WHITE,
        )

        key_t.next_to(header, DOWN, buff=0.5)

        data_big = T(
            "DỮ  LIỆU",
            60,
            HIGHLIGHT,
            weight=BOLD,
        )

        data_big.move_to(DOWN * 0.35)

        with self.voiceover(
            text="Chìa khóa của phép màu này, một lần nữa, lại nằm ở dữ liệu."
        ) as tr:

            self.play(
                FadeIn(key_t, shift=UP * 0.1),
                run_time=0.5,
            )

            self.play(
                GrowFromCenter(data_big),
                run_time=0.8,
            )

            flash_mob(
                self,
                data_big,
                color=HIGHLIGHT,
                radius=1.5,
            )

            self.wait(max(0, tr.duration - 1.6))

        self.play(
            FadeOut(
                VGroup(
                    key_t,
                    data_big,
                )
            ),
            run_time=0.4,
        )

        # =========================================================
        # 5.7 Data recipe
        # =========================================================
        recipe_title = T(
            "Công thức dữ liệu ProLong:",
            20,
            WHITE,
            weight=BOLD,
        )

        recipe_title.next_to(header, DOWN, buff=0.45)

        long_title = T(
            "① Dữ liệu ngữ cảnh DÀI",
            22,
            ACADEMIA,
            weight=BOLD,
        )

        long_desc = T(
            "Mã nguồn · Notebook · Tài liệu kỹ thuật",
            15,
            GRAY_A,
        )

        long_card = RoundedRectangle(
            corner_radius=0.12,
            width=4.8,
            height=1.3,
            fill_color=ACADEMIA,
            fill_opacity=0.08,
            stroke_color=ACADEMIA,
            stroke_width=2,
        )

        long_block = VGroup(
            long_card,
            VGroup(
                long_title,
                long_desc,
            ).arrange(
                DOWN,
                buff=0.18,
            ),
        )

        long_block.move_to(LEFT * 3.2 + DOWN * 0.25)

        short_title = T(
            "② Dữ liệu ngữ cảnh NGẮN",
            22,
            SUCCESS,
            weight=BOLD,
        )

        short_desc = T(
            "Instruction · QA · Reasoning",
            15,
            GRAY_A,
        )

        short_card = RoundedRectangle(
            corner_radius=0.12,
            width=4.8,
            height=1.3,
            fill_color=SUCCESS,
            fill_opacity=0.08,
            stroke_color=SUCCESS,
            stroke_width=2,
        )

        short_block = VGroup(
            short_card,
            VGroup(
                short_title,
                short_desc,
            ).arrange(
                DOWN,
                buff=0.18,
            ),
        )

        short_block.move_to(RIGHT * 3.2 + DOWN * 0.25)

        plus_sign = T(
            "+",
            42,
            HIGHLIGHT,
            weight=BOLD,
        )

        plus_sign.move_to(DOWN * 0.25)

        result_box = RoundedRectangle(
            corner_radius=0.12,
            width=7.0,
            height=0.9,
            fill_color=HIGHLIGHT,
            fill_opacity=0.10,
            stroke_color=HIGHLIGHT,
            stroke_width=2,
        )

        result_txt = T(
            "Duy trì năng lực suy luận ở ngữ cảnh dài",
            20,
            HIGHLIGHT,
            weight=BOLD,
        )

        result = VGroup(
            result_box,
            result_txt,
        )

        result.move_to(DOWN * 1.8)

        with self.voiceover(
                text="Phát hiện quan trọng của dự án chỉ ra rằng: sự kết hợp chiến lược giữa dữ liệu "
                     "ngữ cảnh dài chất lượng cao (như mã nguồn và các tệp notebook) cùng với dữ liệu "
                     "ngữ cảnh ngắn chất lượng cao chính là yếu tố quyết định để duy trì năng lực "
                     "suy luận của mô hình."
        ) as tr:

            self.play(
                FadeIn(recipe_title),
                run_time=0.4,
            )

            # "...dữ liệu ngữ cảnh dài chất lượng cao..."
            self.play(
                FadeIn(long_block, shift=UP * 0.2),
                run_time=1.0,
            )

            # "...cùng với dữ liệu ngữ cảnh ngắn chất lượng cao..."
            self.play(
                FadeIn(short_block, shift=UP * 0.2),
                FadeIn(plus_sign),
                run_time=1.0,
            )

            # "...chính là yếu tố quyết định..."
            self.play(
                AnimationGroup(
                    long_block.animate.shift(RIGHT * 0.8),
                    short_block.animate.shift(LEFT * 0.8),
                    lag_ratio=0,
                ),
                run_time=0.8,
            )

            self.bring_to_front(plus_sign)

            self.play(
                FadeIn(result, scale=0.9),
                run_time=0.8,
            )

            flash_mob(
                self,
                result,
                color=HIGHLIGHT,
                radius=1.2,
            )

            self.wait(max(0, tr.duration - 3.6))

        self.play(
            FadeOut(
                VGroup(
                    recipe_title,
                    long_block,
                    short_block,
                    plus_sign,
                    result,
                )
            ),
            run_time=0.4,
        )

        # =========================================================
        # 5.8 Summary of all projects
        # =========================================================
        sum_title = T(
            "Tổng kết — Bốn công trình học thuật:",
            21,
            WHITE,
            weight=BOLD,
        )

        sum_title.next_to(header, DOWN, buff=0.45)

        proj_data = [
            (
                "Curating",
                "Pairwise quality scoring",
                ACADEMIA,
            ),
            (
                "WebOrganizer",
                "Topic × Format classification",
                HIGHLIGHT,
            ),
            (
                "RegMix",
                "Domain mix optimization (ICLR)",
                SUCCESS,
            ),
            (
                "ProLong",
                "Long context, 5% Meta's resources",
                INDUSTRY,
            ),
        ]

        proj_cards = VGroup()

        for name, desc, col in proj_data:

            bg = RoundedRectangle(
                corner_radius=0.10,
                width=6.8,
                height=0.8,
                fill_color=col,
                fill_opacity=0.12,
                stroke_color=col,
                stroke_width=1.2,
            )

            nt = T(
                name,
                20,
                col,
                weight=BOLD,
            )

            dt = T(
                desc,
                14,
                GRAY_A,
            )

            nt.move_to([-2.0, 0, 0])
            dt.move_to([1.5, 0, 0])

            proj_cards.add(
                VGroup(
                    bg,
                    nt,
                    dt,
                )
            )

        proj_cards.arrange(
            DOWN,
            buff=0.14,
        )

        proj_cards.move_to(DOWN * 0.55)

        budget_badge = T(
            "Tất cả vận hành trong ngân sách học thuật giới hạn",
            20,
            SUCCESS,
            weight=BOLD,
        )

        budget_badge.next_to(
            proj_cards,
            DOWN,
            buff=0.24,
        )

        with self.voiceover(
            text="Tất cả những công trình này — từ Curating, WebOrganizer, Regmix cho đến PROLONG — "
                 "đều là những bài báo thuần học thuật vận hành nghiêm túc trong ngân sách giới hạn. "
                 "Giới học thuật mới chỉ bắt đầu chạm vào bề nổi của đại dương tri thức dữ liệu."
        ) as tr:

            self.play(
                FadeIn(sum_title),
                run_time=0.4,
            )

            self.play(
                LaggedStart(
                    *[
                        FadeIn(
                            c,
                            shift=RIGHT * 0.15,
                        )
                        for c in proj_cards
                    ],
                    lag_ratio=0.25,
                ),
                run_time=min(
                    1.8,
                    tr.duration * 0.55,
                ),
            )

            self.play(
                FadeIn(
                    budget_badge,
                    shift=UP * 0.1,
                ),
                run_time=0.5,
            )

            flash_mob(
                self,
                budget_badge,
                color=SUCCESS,
                radius=1.5,
            )

            self.wait(max(0, tr.duration - 3.2))

        self.play(
            FadeOut(
                VGroup(
                    sum_title,
                    proj_cards,
                    budget_badge,
                )
            ),
            run_time=0.4,
        )

        # =========================================================
        # 5.9 Open questions + scaling laws
        # =========================================================
        oq_title = T(
            "Câu hỏi mở và hướng nghiên cứu tiếp theo:",
            21,
            WHITE,
            weight=BOLD,
        )

        oq_title.next_to(header, DOWN, buff=0.45)

        oq_items = VGroup(
            T(
                "▸  Công cụ hiện tại còn thô sơ",
                24,
                WHITE,
            ),
            T(
                "▸  Tương tác: chất lượng dữ liệu ↔ Scaling Laws",
                24,
                HIGHLIGHT,
            ),
            T(
                "▸  Nghiên cứu dữ liệu = nền móng tác động AI",
                24,
                SUCCESS,
                weight=BOLD,
            ),
        )

        oq_items.arrange(
            DOWN,
            buff=0.30,
            aligned_edge=LEFT,
        )

        oq_items.next_to(
            oq_title,
            DOWN,
            buff=1,
        )

        with self.voiceover(
            text="Dù các công cụ hiện tại còn thô sơ và nhiều câu hỏi mở về sự tương tác giữa chất "
                 "lượng dữ liệu với quy luật mở rộng (Scaling laws) vẫn chưa có lời giải, nhưng có "
                 "một điều chắc chắn: nghiên cứu dữ liệu tiền huấn luyện chính là nền móng vững chắc "
                 "nhất để học thuật tạo ra những tác động thay đổi cục diện công nghệ AI."
        ) as tr:

            self.play(
                FadeIn(oq_title),
                run_time=0.4,
            )

            self.play(
                LaggedStart(
                    *[
                        FadeIn(
                            it,
                            shift=LEFT * 0.12,
                        )
                        for it in oq_items
                    ],
                    lag_ratio=0.35,
                ),
                run_time=min(
                    1.8,
                    tr.duration * 0.55,
                ),
            )

            self.wait(max(0, tr.duration - 2.5))

        self.wait(0.8)

        clear(self)
# ══════════════════════════════════════════════════════════════════════════════
# Scene 6 — P4_PostTraining
# ══════════════════════════════════════════════════════════════════════════════
class P4_PostTraining(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ── 6.1 Transition: post-training ────────────────────────────────────
        hdr_bg  = RoundedRectangle(corner_radius=0.2, width=8.2, height=1.0,
                                    color=ACADEMIA, fill_color=ACADEMIA,
                                    fill_opacity=0.12, stroke_width=2)
        hdr_txt = title_card("TRỤ CỘT 3: POST-TRAINING", size=28)
        header  = VGroup(hdr_bg, hdr_txt).shift(UP * 2.7)

        with self.voiceover(
            text="Sau khi giải quyết xong bài toán dữ liệu đầu vào, giới học thuật tiến tới một "
                 "tử địa đắt đỏ hơn: huấn luyện mô hình."
        ) as tr:
            self.play(GrowFromCenter(hdr_bg), Write(hdr_txt), run_time=1.2)
            self.wait(max(0, tr.duration - 1.3))

        # Giants metaphor
        giant_t = T("Tại sao phải tốn triệu đô huấn luyện lại từ đầu,\nkhi có thể đứng trên vai những gã khổng lồ?",
                     20, HIGHLIGHT)
        giant_t.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
            text="Nhưng tại sao chúng ta phải bỏ hàng triệu đô-la để huấn luyện lại từ đầu "
                 "(Pre-training), trong khi hoàn toàn có thể đứng trên vai những gã khổng lồ?"
        ) as tr:
            self.play(FadeIn(giant_t, shift=UP * 0.1), run_time=0.7)
            self.wait(max(0, tr.duration - 0.9))

        self.play(FadeOut(giant_t))

        # ── 6.2 Open-weight strategy ──────────────────────────────────────────
        ow_title = T("Chiến lược: Tận dụng Open-weight Models", 21, SUCCESS, weight=BOLD)
        ow_title.next_to(header, DOWN, buff=0.45)

        ow_models = VGroup(
            T("Llama  (Meta)", 20, ACADEMIA, weight=BOLD),
            T("Gemma  (Google)", 20, SUCCESS, weight=BOLD),
            T("Mistral  (Mistral AI)", 20, HIGHLIGHT, weight=BOLD),
        ).arrange(DOWN, buff=0.32)
        ow_models.move_to(DOWN * 0.65)

        with self.voiceover(
            text="Chiến lược ở đây là tận dụng các Mô hình trọng số mở (Open-weight models) như "
                 "Llama hay Mistral để làm tinh chỉnh và căn chỉnh hành vi."
        ) as tr:
            self.play(FadeIn(ow_title))
            self.play(
                LaggedStart(*[FadeIn(m, shift=RIGHT * 0.18) for m in ow_models],
                            lag_ratio=0.3),
                run_time=min(1.4, tr.duration * 0.6)
            )
            self.wait(max(0, tr.duration - 1.8))

        self.play(FadeOut(VGroup(ow_title, ow_models)))

        # ── 6.3 Preference Optimization rises ─────────────────────────────────
        pref_banner = T("Preference Optimization lên ngôi!", 26, HIGHLIGHT, weight=BOLD)
        pref_banner.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
            text="Lúc này, kỹ thuật Tối ưu hóa phản hồi (Preference Optimization) lên ngôi."
        ) as tr:
            self.play(GrowFromCenter(pref_banner), run_time=0.7)
            flash_mob(self, pref_banner, color=HIGHLIGHT, radius=1.2)
            self.wait(max(0, tr.duration - 1.0))

        self.play(FadeOut(pref_banner))

        # ── 6.4 Tiger vs Squirrel example ────────────────────────────────────
        pref_title = T("Dữ liệu cặp phản hồi — Preference Pairs:", 20, WHITE)
        pref_title.next_to(header, DOWN, buff=0.45)

        prompt_bg  = RoundedRectangle(corner_radius=0.12, width=6.8, height=0.68,
                                      fill_color="#12122a", fill_opacity=0.9,
                                      stroke_color=NEUTRAL, stroke_width=1.5)
        prompt_t   = T("Linh vật của Đại học Princeton là gì?", 17, WHITE)
        prompt_grp = VGroup(prompt_bg, prompt_t).move_to(UP * 0.75)

        win_bg    = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.5,
                                     fill_color=SUCCESS, fill_opacity=0.15,
                                     stroke_color=SUCCESS, stroke_width=2)
        win_title = T("Con Hổ", 22, SUCCESS, weight=BOLD)
        win_sub   = T('"fierce spirit"', 13, GRAY_A)
        win_sub.next_to(win_title, DOWN, buff=0.1)
        win_check = VGroup(
            T("✓", 13, SUCCESS),
            T("y_w", 18, SUCCESS),
            T("(winning)", 13, SUCCESS),
        ).arrange(RIGHT, buff=0.07)
        win_check.move_to([0, -win_bg.height/2 + 0.22, 0])
        win_card  = VGroup(win_bg, win_title, win_sub, win_check).move_to(LEFT * 2.5 + DOWN * 0.95)

        lose_bg   = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.5,
                                      fill_color=INDUSTRY, fill_opacity=0.15,
                                      stroke_color=INDUSTRY, stroke_width=2)
        lose_title = T("Con Sóc", 22, INDUSTRY, weight=BOLD)
        lose_sub   = T('"wise squirrel"', 13, GRAY_A)
        lose_sub.next_to(lose_title, DOWN, buff=0.1)
        lose_x = VGroup(
            T("✗", 13, INDUSTRY),
            T("y_l", 18, INDUSTRY),
            T("(losing)", 13, INDUSTRY),
        ).arrange(RIGHT, buff=0.07)
        lose_x.move_to([0, -lose_bg.height/2 + 0.22, 0])
        lose_card  = VGroup(lose_bg, lose_title, lose_sub, lose_x).move_to(RIGHT * 2.5 + DOWN * 0.95)

        arr_w = Arrow(prompt_grp.get_bottom(), win_card.get_top() + RIGHT * 0.2,
                      buff=0.08, color=SUCCESS, stroke_width=2.0,
                      max_tip_length_to_length_ratio=0.15)
        arr_l = Arrow(prompt_grp.get_bottom(), lose_card.get_top() + LEFT * 0.2,
                      buff=0.08, color=INDUSTRY, stroke_width=2.0,
                      max_tip_length_to_length_ratio=0.15)

        prob_t = T("P(y_w | x)  UP     P(y_l | x)  DOWN", 22, WHITE)
        prob_t.move_to(DOWN * 2.42)

        with self.voiceover(
            text="Thuật toán sẽ sử dụng các cặp dữ liệu so sánh, ví dụ như với câu lệnh: "
                 "'Linh vật của đại học Princeton là gì?', mô hình sẽ học cách ưu tiên câu trả lời "
                 "đúng là 'Con Hổ' và loại bỏ câu trả lời sai là 'Con Sóc'."
        ) as tr:
            self.play(FadeIn(pref_title))
            self.play(Create(prompt_bg), Write(prompt_t), run_time=0.6)
            self.play(GrowArrow(arr_w), FadeIn(win_card, shift=DOWN * 0.2), run_time=0.7)
            self.play(GrowArrow(arr_l), FadeIn(lose_card, shift=DOWN * 0.2), run_time=0.7)
            self.play(FadeIn(prob_t, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0, tr.duration - 3.2))

        self.play(FadeOut(VGroup(pref_title, prompt_grp, win_card, lose_card,
                                  arr_w, arr_l, prob_t)))

        # ── 6.5 DPO vs SimPO intro ────────────────────────────────────────────
        vs_title = T("DPO (Stanford)  vs  SimPO (Princeton)", 22, WHITE, weight=BOLD)
        vs_title.next_to(header, DOWN, buff=0.45)

        with self.voiceover(
            text="Nếu như trước đây, khối công nghiệp thống trị bằng phương pháp DPO cồng kềnh từ "
                 "Stanford, thì năm vừa qua, phòng lab Princeton đã tạo nên một bước ngoặt với "
                 "thuật toán SimPO."
        ) as tr:
            self.play(FadeIn(vs_title, shift=DOWN * 0.1), run_time=0.7)
            self.wait(max(0, tr.duration - 0.9))

        self.play(FadeOut(vs_title))

        # ── 6.6 DPO formula ───────────────────────────────────────────────────
        dpo_title = T("DPO — Direct Preference Optimization", 22, INDUSTRY, weight=BOLD)
        dpo_title.next_to(header, DOWN, buff=0.45)
        dpo_src   = T("Rafailov et al., NeurIPS 2023  ·  Stanford", 14, NEUTRAL)
        dpo_src.next_to(dpo_title, DOWN, buff=0.32)

        formula_rows = VGroup(
            T("L_DPO = -E [ log sigmoid(", 18, WHITE),
            T("beta log policy(y_w | x) / reference(y_w | x)", 16, SUCCESS),
            T("- beta log policy(y_l | x) / reference(y_l | x)", 16, INDUSTRY),
            T(") ]", 18, WHITE),
        ).arrange(DOWN, buff=0.08)
        formula_rows[1].set_color(SUCCESS)
        formula_rows[2].set_color(INDUSTRY)
        formula_rows.next_to(dpo_src, DOWN, buff=0.38)

        dpo_box = SurroundingRectangle(
            formula_rows, corner_radius=0.14,
            color=INDUSTRY, fill_color=INDUSTRY, fill_opacity=0.08, buff=0.28
        )

        legend_items = VGroup(
            VGroup(
                T("policy", 17, SUCCESS),
                T(" = policy (mô hình đang học)", 13, WHITE),
            ).arrange(RIGHT, buff=0.10),
            VGroup(
                T("reference", 17, INDUSTRY),
                T(" = reference model (cố định — tốn bộ nhớ!)", 13, WHITE),
            ).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        legend_items.next_to(dpo_box, DOWN, buff=0.20)

        with self.voiceover(
            text="Bằng cách loại bỏ hoàn toàn mô hình tham chiếu phức tạp và đưa vào cơ chế chuẩn "
                 "hóa độ dài, SimPO sử dụng một công thức toán học tối giản để ép mô hình chọn ra "
                 "câu trả lời chất lượng nhất một cách vô cùng nhẹ nhàng."
        ) as tr:
            self.play(FadeIn(dpo_title), FadeIn(dpo_src), run_time=0.6)
            self.play(Create(dpo_box), run_time=0.4)
            self.play(FadeIn(formula_rows[0]), run_time=0.4)
            self.play(FadeIn(formula_rows[1]), run_time=0.4)
            self.play(FadeIn(formula_rows[2]), FadeIn(formula_rows[3]), run_time=0.4)
            self.play(
                LaggedStart(*[FadeIn(it) for it in legend_items], lag_ratio=0.3),
                run_time=0.7
            )
            self.wait(max(0, tr.duration - 3.0))

        self.play(FadeOut(VGroup(dpo_title, dpo_src, dpo_box, formula_rows, legend_items)))

        # ── 6.7 SimPO impact statement ────────────────────────────────────────
        impact_t = T("SimPO tạo nên một cú sốc lớn!", 26, SUCCESS, weight=BOLD)
        impact_t.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
            text="Hiệu quả thực tế của thuật toán SimPO đã tạo nên một cú sốc lớn."
        ) as tr:
            self.play(GrowFromCenter(impact_t), run_time=0.7)
            flash_mob(self, impact_t, color=SUCCESS, radius=1.3)
            self.wait(max(0, tr.duration - 1.0))

        self.play(FadeOut(impact_t))

        # ── 6.8 Training recipe ───────────────────────────────────────────────
        recipe_title = T("Công thức huấn luyện SimPO:", 21, WHITE)
        recipe_title.next_to(header, DOWN, buff=0.45)

        gemma_box = RoundedRectangle(corner_radius=0.14, width=7.5, height=1.5,
                                      fill_color=ACADEMIA, fill_opacity=0.12,
                                      stroke_color=ACADEMIA, stroke_width=1.5)
        gemma_box.move_to(DOWN * 0.35)
        r1 = T("Gemma 2-9B  (Google)", 19, ACADEMIA, weight=BOLD)
        r2 = T("50.000 câu lệnh mẫu", 17, WHITE)
        r3 = T("< 2 tiếng  ·  8 GPU  →  Gần như không tốn gì!", 17, SUCCESS, weight=BOLD)
        VGroup(r1, r2, r3).arrange(DOWN, buff=0.22).move_to(gemma_box.get_center())

        with self.voiceover(
            text="Khi áp dụng trên mô hình Gemma 2-9B của Google với chỉ 50.000 câu lệnh mẫu, "
                 "thuật toán SimPO chỉ mất chưa đầy 2 tiếng đồng hồ chạy trên 8 GPU — một mức "
                 "ngân sách tính toán gần như bằng không của phòng lab đại học."
        ) as tr:
            self.play(FadeIn(recipe_title))
            self.play(FadeIn(gemma_box), run_time=0.5)
            self.play(
                LaggedStart(FadeIn(r1), FadeIn(r2), FadeIn(r3), lag_ratio=0.3),
                run_time=1.0
            )
            flash_mob(self, r3, color=SUCCESS, radius=1.2)
            self.wait(max(0, tr.duration - 2.5))

        self.play(FadeOut(VGroup(recipe_title, gemma_box, r1, r2, r3)))

        # ── 6.9 ChatBot Arena leaderboard ────────────────────────────────────
        arena_title = T("Gemma-2-9b-it-SimPO trên ChatBot Arena:", 21, WHITE)
        arena_title.next_to(header, DOWN, buff=0.4)

        with self.voiceover(
            text="Nhưng khi đưa lên Chatbot Arena — bảng xếp hạng uy tín nhất do người dùng trực "
                 "tiếp đánh giá — mô hình Gemma-2-SimPO lập tức nhảy vọt 18 bậc, trở thành mô hình "
                 "mạnh mẽ nhất thế giới trong phân khúc dưới 10 tỷ tham số và thu về hơn 1,2 triệu "
                 "lượt tải xuống."
        ) as tr:
            self.play(FadeIn(arena_title), run_time=0.5)
            self.wait(max(0, tr.duration - 0.7))

        # Leaderboard rows
        ROW_H    = 0.38
        ROW_GAP  = 0.09
        SLOT     = ROW_H + ROW_GAP
        DOTS_H   = 0.24
        DOTS_GAP = 0.09
        bx       = 0.3

        y30    =  0.92
        y33    =  y30 - SLOT
        y35    =  y33 - SLOT
        y_dots =  y35 - (ROW_H / 2 + DOTS_GAP + DOTS_H / 2)
        y46    =  y_dots - (DOTS_H / 2 + DOTS_GAP + ROW_H / 2)
        y49    =  y46 - SLOT
        y31    =  y30 - SLOT

        def make_row(rank_str, name_str, col, hl=False):
            bg = RoundedRectangle(corner_radius=0.07, width=6.4, height=ROW_H,
                                  fill_color=col,
                                  fill_opacity=0.45 if hl else 0.12,
                                  stroke_color=col,
                                  stroke_width=2.2 if hl else 0.5)
            rk = T(f"#{rank_str}", 14, col if hl else GRAY_C,
                   weight=BOLD if hl else NORMAL)
            nm = T(name_str, 13, WHITE if hl else GRAY_B)
            rk.move_to([-2.6, 0, 0])
            nm.move_to([ 0.5, 0, 0])
            return VGroup(bg, rk, nm)

        row30 = make_row("30", "Gemma-2-27b-it",    GRAY_C).move_to([bx, y30,    0])
        row33 = make_row("33", "Deepseek-Coder-v2", GRAY_C).move_to([bx, y33,    0])
        row35 = make_row("35", "Yi-Large",           GRAY_C).move_to([bx, y35,    0])

        dots_bg = RoundedRectangle(corner_radius=0.05, width=6.4, height=0.28,
                                   fill_color=GRAY_E, fill_opacity=0.08,
                                   stroke_color=GRAY_C, stroke_width=0.5, stroke_opacity=0.5)
        dots_tx = T("⋮   ( #36 – #45 )   ⋮", 11, GRAY_C)
        dots    = VGroup(dots_bg, dots_tx).move_to([bx, y_dots, 0])

        row46 = make_row("46", "Qwen2-72B-Instruct", GRAY_C).move_to([bx, y46, 0])
        row49 = make_row("49", "Gemma-2-9b-it",      ORANGE, hl=True).move_to([bx, y49, 0])

        static_rows = VGroup(row30, row33, row35, dots, row46)

        self.play(
            LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in static_rows],
                        lag_ratio=0.12),
            run_time=1.0
        )
        self.play(FadeIn(row49, shift=DOWN * 0.1), run_time=0.4)
        flash_mob(self, row49, color=ORANGE, radius=0.7)
        self.wait(0.5)

        # Jump animation: rank 49 → 31
        row31_final = make_row("31", "Gemma-2-9b-it-SimPO", SUCCESS, hl=True)
        row31_final.move_to([bx, y31, 0])
        PUSH = SLOT

        row49.set_z_index(10)
        self.play(
            row49.animate.move_to([bx, y31, 0]),
            row33.animate.shift(DOWN * PUSH),
            row35.animate.shift(DOWN * PUSH),
            dots .animate.shift(DOWN * PUSH),
            FadeOut(row46),
            run_time=1.35, rate_func=rush_from
        )
        row49.set_z_index(0)
        self.play(Transform(row49, row31_final), run_time=0.40)

        badge_txt = T("+18", 28, SUCCESS, weight=BOLD)
        badge_bg  = Circle(radius=0.42, fill_color=SUCCESS, fill_opacity=0.18,
                            stroke_color=SUCCESS, stroke_width=2.2)
        badge = VGroup(badge_bg, badge_txt)
        badge.next_to(row49, LEFT, buff=0.20)
        self.play(GrowFromCenter(badge), run_time=0.55)
        flash_mob(self, badge, color=SUCCESS, radius=0.65)

        # Trophy stats
        trophy_t = T("Mô hình mạnh nhất < 10B · 1,2 triệu lượt tải", 15, HIGHLIGHT, weight=BOLD)
        trophy_t.next_to(dots, DOWN, buff=0.32)
        self.play(FadeIn(trophy_t, shift=UP * 0.1), run_time=0.6)
        flash_mob(self, trophy_t, color=HIGHLIGHT, radius=1.4)
        self.wait(0.8)

        self.play(FadeOut(VGroup(arena_title, row30, row33, row35, dots, row49,
                                  badge, trophy_t)))

        # ── 6.10 Deep thinking — not just numbers ─────────────────────────────
        deep_t = T("Đỉnh cao tư duy học thuật không dừng lại ở những con số!", 19, ACADEMIA, weight=BOLD)
        deep_t.next_to(header, DOWN, buff=0.5)

        with self.voiceover(
            text="Tuy nhiên, đỉnh cao tư duy học thuật không dừng lại ở những con số chuyển động."
        ) as tr:
            self.play(FadeIn(deep_t, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0, tr.duration - 0.8))

        self.play(FadeOut(deep_t))

        # ── 6.11 Open questions ───────────────────────────────────────────────
        open_title = T("Câu hỏi mở — Lật ngược vấn đề:", 22, WHITE, weight=BOLD)
        open_title.next_to(header, DOWN, buff=0.45)

        questions_open = VGroup(
            T("① SimPO trên Llama 3 vs Gemma 2: tại sao forgetting khác nhau?", 20, WHITE),
            T("② RL reasoning: tại sao Qwen 2.5 base, không phải Llama 3?", 20, WHITE),
            T("③ Thế giới thiếu controlled studies: base × data × algorithm", 20, HIGHLIGHT),
            T("④ Cần hiểu hộp đen trước khi mơ về mở rộng quy mô!", 20, INDUSTRY),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        questions_open.move_to(DOWN * 0.85)

        with self.voiceover(
            text="Giới nghiên cứu tiếp tục đặt câu hỏi lật ngược vấn đề: Tại sao cùng một thuật "
                 "toán SimPO khi chạy trên nền Llama 3 và Gemma 2 lại cho ra những hiện tượng quên "
                 "kiến thức khác nhau?"
        ) as tr:
            self.play(FadeIn(open_title))
            self.play(FadeIn(questions_open[0], shift=RIGHT * 0.12), run_time=0.6)
            self.wait(max(0, tr.duration - 0.9))

        with self.voiceover(
            text="Tại sao xu hướng học tăng cường cho lập luận hiện tại đều chọn Qwen 2.5 làm gốc "
                 "chứ không phải Llama 3?"
        ) as tr:
            self.play(FadeIn(questions_open[1], shift=RIGHT * 0.12), run_time=0.5)
            self.wait(max(0, tr.duration - 0.7))

        with self.voiceover(
            text="Học thuật chỉ ra rằng: thế giới đang thiếu những nghiên cứu kiểm soát toàn diện "
                 "(controlled studies) về mối tương tác giữa mô hình nền, dữ liệu và thuật toán "
                 "hậu huấn luyện."
        ) as tr:
            self.play(FadeIn(questions_open[2], shift=RIGHT * 0.12), run_time=0.6)
            self.wait(max(0, tr.duration - 0.9))

        with self.voiceover(
            text="Chúng ta cần hiểu rõ bản chất sâu xa của những chiếc hộp đen này trước khi mơ "
                 "về việc mở rộng quy mô."
        ) as tr:
            self.play(FadeIn(questions_open[3], shift=RIGHT * 0.12), run_time=0.6)
            self.wait(max(0, tr.duration - 0.9))

        self.play(FadeOut(VGroup(open_title, questions_open)))

        # ── 6.12 Closing statement ────────────────────────────────────────────
        closing_bg = RoundedRectangle(corner_radius=0.2, width=11.0, height=2.8,
                                       fill_color=ACADEMIA, fill_opacity=0.10,
                                       stroke_color=ACADEMIA, stroke_width=2)
        closing_bg.move_to(ORIGIN)

        closing1 = T("Một thuật toán thông minh, tinh gọn", 24, WHITE)
        closing2 = T("được thực thi đúng cách", 28, HIGHLIGHT, weight=BOLD)
        closing3 = T("hoàn toàn có thể san phẳng khoảng cách tài nguyên hàng triệu đô-la.", 20, SUCCESS, weight=BOLD)
        closing4 = T("— Danqi Chen, ICLR 2025", 16, NEUTRAL)
        closing  = VGroup(closing1, closing2, closing3, closing4).arrange(DOWN, buff=0.22)
        closing.move_to(ORIGIN)

        with self.voiceover(
            text="Chính tư duy luôn đào sâu vào bản chất khoa học đó đã chứng minh một chân lý: "
                 "Một thuật toán thông minh, tinh gọn được thực thi đúng cách hoàn toàn có thể "
                 "san phẳng khoảng cách tài nguyên hàng triệu đô-la."
        ) as tr:
            self.play(FadeIn(closing_bg), run_time=0.6)
            self.play(
                LaggedStart(*[FadeIn(line, shift=UP * 0.1) for line in closing],
                            lag_ratio=0.3),
                run_time=1.5
            )
            flash_mob(self, closing2, color=HIGHLIGHT, radius=2.0)
            self.wait(max(0, tr.duration - 2.5))

        self.wait(1.2)
        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# P4_Complete — All 6 scenes stitched together with chapter-break transitions
# Render: manim -pqh part4.py P4_Complete
# ══════════════════════════════════════════════════════════════════════════════
class P4_Complete(VoiceoverScene):
    """
    Single continuous Part-4 video (≈ 8 min).
    Sequences all 6 scenes with cinematic chapter-break transitions.

    Each sub-scene's construct() calls set_speech_service() on the way in;
    we disable that at the instance level after the first real initialisation
    so the TTS service is shared and audio caches are not regenerated.
    """

    def construct(self):
        # ── One-time speech-service initialisation ────────────────────────
        self.set_speech_service(svc())

        # Lock out re-initialisation from sub-scene constructs
        # (instance attribute shadows the inherited class method)
        self.set_speech_service = lambda *a, **kw: None  # type: ignore[assignment]

        # ── Scene 1: Pre-training Data Curation ───────────────────────────
        P4_DataCuration.construct(self)

        # ── Scene 2: Curating Project ─────────────────────────────────────
        P4_CuratingProject.construct(self)

        # ── Scene 3: WebOrganizer ─────────────────────────────────────────
        P4_WebOrganizer.construct(self)

        # ── Scene 4: RegMix Results ───────────────────────────────────────
        P4_RegmixResults.construct(self)

        # ── Scene 5: ProLong ──────────────────────────────────────────────
        P4_Prolong.construct(self)

        # ── Scene 6: Post-Training ────────────────────────────────────────
        P4_PostTraining.construct(self)
