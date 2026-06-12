"""
Phần 5: Lời kêu gọi — Học thuật ✕ Tương lai AI
Manim Community v0.20.1 | Voice: vi-VN-NamMinhNeural
Render: manim -pqh part5.py P5_Complete
"""
from __future__ import annotations
import random, sys, os
import numpy as np
from manim import *
from manim.utils.rate_functions import ease_in_quad, ease_out_quad
from manim_voiceover import VoiceoverScene
sys.path.insert(0, os.path.dirname(__file__))
from edge_service import EdgeTTSService

# ── constants ─────────────────────────────────────────────────────────────────
FONT      = "Be Vietnam Pro"
ACADEMIA  = BLUE_C
INDUSTRY  = RED_C
HIGHLIGHT = YELLOW_C
SUCCESS   = GREEN_C
NEUTRAL   = GRAY_C
VOICE     = "vi-VN-NamMinhNeural"

# ── helpers ───────────────────────────────────────────────────────────────────
def svc():
    return EdgeTTSService(voice=VOICE)


def T(text: str, font_size: int = 24, color=WHITE, **kw) -> Text:
    return Text(text, font=FONT, font_size=font_size, color=color, **kw)


def clear(scene, run_time: float = 0.5) -> None:
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)


def flash_mob(scene, mob, color=YELLOW_C, radius: float = 0.5) -> None:
    scene.play(Flash(mob, color=color, flash_radius=radius, run_time=0.45))


def mk_rbox(label: str, w: float, h: float, color, fs: int = 14) -> VGroup:
    """Rounded rectangle with centered bold label."""
    bg  = RoundedRectangle(corner_radius=0.16, width=w, height=h,
                            color=color, fill_color=color, fill_opacity=0.15)
    lbl = T(label, fs, color, weight=BOLD).move_to(bg)
    return VGroup(bg, lbl)


def sota_badge() -> VGroup:
    ring = Circle(radius=0.40, color=HIGHLIGHT,
                  fill_color=HIGHLIGHT, fill_opacity=0.22, stroke_width=2.8)
    txt  = T("SOTA", 12, HIGHLIGHT, weight=BOLD).move_to(ring)
    return VGroup(ring, txt)


def chapter_break(scene, title: str, subtitle: str = None, color=ACADEMIA) -> None:
    bar     = Line(LEFT * 4.4, RIGHT * 4.4, color=color, stroke_width=2.8)
    title_m = T(title, 26, WHITE, weight=BOLD)
    title_m.next_to(bar, UP, buff=0.28)
    items = [bar, title_m]
    if subtitle:
        sub_m = T(subtitle, 14, color)
        sub_m.next_to(bar, DOWN, buff=0.22)
        items.append(sub_m)
    scene.play(GrowFromCenter(bar), run_time=0.35)
    scene.play(FadeIn(title_m, shift=DOWN * 0.10), run_time=0.38)
    if subtitle:
        scene.play(FadeIn(sub_m, shift=UP * 0.07), run_time=0.28)
    scene.wait(0.52)
    scene.play(VGroup(*items).animate.shift(RIGHT * 12),
               run_time=0.38, rate_func=rush_into)
    scene.remove(*items)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 — P5_RLReasoning  (00:00 → 00:54)
# CSV rows 114–117  |  4 voiceovers
# ══════════════════════════════════════════════════════════════════════════════
class P5_RLReasoning(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ============================================================
        # PART 1
        # RL FOR REASONING
        # ============================================================

        hdr = T(
            "HỌC TĂNG CƯỜNG CHO SUY LUẬN",
            28,
            HIGHLIGHT,
            weight=BOLD,
        ).shift(UP * 2.8)

        sub = T(
            "Reinforcement Learning for Reasoning",
            16,
            NEUTRAL,
        ).next_to(hdr, DOWN, buff=0.15)

        intro = T(
            "Làm thế nào để AI học cách suy nghĩ tốt hơn?",
            20,
            WHITE,
            weight=BOLD,
        ).shift(UP * 1.6)

        with self.voiceover(
            """
            Trước khi khép lại hành trình Princeton NLP,
            hãy nhìn vào một trong những hướng nghiên cứu
            quan trọng nhất của AI hiện đại.

            Một câu hỏi tưởng như rất đơn giản:
            làm thế nào để mô hình không chỉ ghi nhớ kiến thức,
            mà còn học được cách suy luận ngày càng tốt hơn?
            """
        ):
            self.play(
                FadeIn(hdr, shift=DOWN * 0.2),
                FadeIn(sub),
                run_time=0.8,
            )

            self.play(
                Write(intro),
                run_time=1.5,
            )

            self.wait(0.5)

        self.play(
            FadeOut(intro),
            run_time=0.4,
        )

        # ------------------------------------------------

        n_q = mk_rbox(
            "Bài toán\nhình thức",
            2.6,
            0.85,
            ACADEMIA,
        ).shift(LEFT * 5.0)

        n_p = mk_rbox(
            "Policy\n(Mô hình LM)",
            2.8,
            0.85,
            HIGHLIGHT,
        ).shift(LEFT * 1.7)

        n_reason = mk_rbox(
            "Các bước\nsuy luận",
            2.8,
            0.85,
            NEUTRAL,
        ).shift(RIGHT * 1.7)

        n_v = mk_rbox(
            "LEAN\nVerifier",
            2.5,
            0.85,
            SUCCESS,
        ).shift(RIGHT * 5.0)

        aq = Arrow(
            n_q.get_right(),
            n_p.get_left(),
            buff=0.12,
            color=NEUTRAL,
        )

        ap = Arrow(
            n_p.get_right(),
            n_reason.get_left(),
            buff=0.12,
            color=NEUTRAL,
        )

        ar = Arrow(
            n_reason.get_right(),
            n_v.get_left(),
            buff=0.12,
            color=NEUTRAL,
        )

        with self.voiceover(
            """
            Ý tưởng của học tăng cường cho suy luận khá trực quan.

            Đầu tiên, hệ thống được giao một bài toán hình thức,
            chẳng hạn như một định lý toán học cần chứng minh.
            """
        ):
            self.play(
                FadeIn(n_q, scale=0.85),
                run_time=0.8,
            )

        with self.voiceover(
            """
            Bài toán này được đưa vào mô hình ngôn ngữ,
            đóng vai trò policy.

            Nhiệm vụ của policy là đề xuất những hướng giải quyết
            và những chuỗi suy luận có thể dẫn tới đáp án.
            """
        ):
            self.play(
                GrowArrow(aq),
                FadeIn(n_p, scale=0.85),
                run_time=1.0,
            )

        with self.voiceover(
            """
            Thay vì chỉ tạo ra một đáp án cuối cùng,
            mô hình còn sinh ra toàn bộ quá trình suy nghĩ
            từng bước một.
            """
        ):
            self.play(
                GrowArrow(ap),
                FadeIn(n_reason, scale=0.85),
                run_time=1.0,
            )

        with self.voiceover(
            """
            Những bước suy luận này sau đó được chuyển tới
            bộ kiểm chứng hình thức Lean.

            Đây là nơi hệ thống kiểm tra:
            liệu lập luận có thực sự đúng về mặt logic hay không.
            """
        ):
            self.play(
                GrowArrow(ar),
                FadeIn(n_v, scale=0.85),
                run_time=1.2,
            )

        # ------------------------------------------------
        # Reward phase
        # ------------------------------------------------

        good = T(
            "✓ Chứng minh hợp lệ",
            18,
            SUCCESS,
            weight=BOLD,
        ).shift(DOWN * 0.9 + RIGHT * 3.8)

        bad = T(
            "✗ Chứng minh thất bại",
            18,
            RED,
            weight=BOLD,
        ).shift(DOWN * 0.9 + RIGHT * 3.8)

        reward = mk_rbox(
            "Reward Signal",
            3.0,
            0.75,
            INDUSTRY,
        ).shift(DOWN * 2.0)

        feed = CurvedArrow(
            reward.get_left(),
            n_p.get_bottom(),
            angle=-1.2,
            color=SUCCESS,
            stroke_width=2.5,
        )

        with self.voiceover(
            """
            Nếu Lean xác nhận lời giải là chính xác,
            mô hình nhận được phần thưởng cao.

            Ngược lại,
            nếu chứng minh thất bại,
            phần thưởng sẽ thấp hoặc bằng không.
            """
        ):
            self.play(
                FadeIn(good),
                run_time=0.6,
            )

            self.wait(5)

            self.play(
                Indicate(good),
                run_time=0.7,
            )

            self.play(
                Transform(good, bad),
                run_time=0.7,
            )

            self.wait(5)

            self.play(
                FadeOut(good),
                run_time=0.7,
            )

            self.play(
                FadeIn(reward, scale=0.9),
                run_time=0.7,
            )

        with self.voiceover(
            """
            Tín hiệu phần thưởng này được đưa ngược trở lại policy.

            Qua hàng triệu vòng lặp như vậy,
            mô hình dần học được những kiểu suy luận hiệu quả hơn,
            và loại bỏ các hướng suy nghĩ sai.
            """
        ):
            self.play(
                Create(feed),
                run_time=1.2,
            )

            self.play(
                Indicate(n_p, color=SUCCESS),
                run_time=0.8,
            )

            self.wait(1)

        clear(self)

        # ============================================================
        # PART 2
        # GOEDEL PROVER
        # ============================================================

        hdr2 = T(
            "GOEDEL PROVER",
            28,
            ACADEMIA,
            weight=BOLD,
        ).shift(UP * 2.8)

        ref2 = T(
            "Princeton · Lean 4 · Lin et al. 2025",
            15,
            NEUTRAL,
        ).next_to(hdr2, DOWN, buff=0.15)

        with self.voiceover(
            """
            Và đây không chỉ là ý tưởng trên giấy.

            Princeton đã hiện thực hóa hướng tiếp cận này
            trong một dự án nổi tiếng mang tên Goedel Prover.
            """
        ):
            self.play(
                FadeIn(hdr2),
                FadeIn(ref2),
                run_time=0.8,
            )

        pipeline = VGroup()

        labels = [
            ("Bài toán", ACADEMIA),
            ("Goedel\nProver", HIGHLIGHT),
            ("Proof", WHITE),
            ("LEAN", SUCCESS),
        ]

        xs = [-4.8, -1.6, 1.6, 4.8]

        boxes = []

        for (txt, col), x in zip(labels, xs):
            b = mk_rbox(txt, 2.2, 0.85, col).shift(RIGHT * x)
            boxes.append(b)

        arrows = VGroup(*[
            Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.1,
                color=NEUTRAL,
            )
            for i in range(3)
        ])

        with self.voiceover(
            """
            Một bài toán được đưa vào Goedel Prover.

            Hệ thống tạo ra bằng chứng,
            sau đó gửi tới Lean để kiểm tra.

            Nếu bằng chứng vượt qua kiểm chứng,
            nó sẽ trở thành dữ liệu huấn luyện mới.
            """
        ):
            self.play(FadeIn(boxes[0]), run_time=0.4)

            for i in range(3):
                self.play(
                    GrowArrow(arrows[i]),
                    FadeIn(boxes[i + 1]),
                    run_time=0.6,
                )

        train_box = mk_rbox(
            "Training",
            2.5,
            0.8,
            INDUSTRY,
        ).shift(DOWN * 1.7)

        loop = CurvedArrow(
            boxes[3].get_bottom(),
            train_box.get_right(),
            angle=-1.2,
            color=INDUSTRY,
        )

        loop2 = CurvedArrow(
            train_box.get_left(),
            boxes[1].get_bottom(),
            angle=-1.2,
            color=SUCCESS,
        )

        with self.voiceover(
            """
            Sau đó toàn bộ quá trình lặp lại.

            Càng giải được nhiều bài toán,
            mô hình càng tích lũy thêm kinh nghiệm suy luận
            cho những bài toán khó hơn phía trước.
            """
        ):
            self.play(
                FadeIn(train_box),
                Create(loop),
                Create(loop2),
                run_time=1.5,
            )

        sota = sota_badge().shift(RIGHT * 5 + UP * 1.6)

        with self.voiceover(
            """
            Kết quả là Goedel Prover đã đạt thành tích
            thuộc nhóm dẫn đầu thế giới
            trong lĩnh vực tạo chứng minh hình thức.
            """
        ):
            self.play(
                FadeIn(sota, scale=0.3),
                run_time=0.5,
            )

            flash_mob(self, sota, radius=0.7)

            self.wait(1)

        clear(self)

        # ============================================================
        # PART 3
        # PRINCETON NLP JOURNEY
        # ============================================================

        title = T(
            "HÀNH TRÌNH PRINCETON NLP",
            25,
            ACADEMIA,
            weight=BOLD,
        ).shift(UP * 2.8)

        self.play(FadeIn(title))

        specs = [
            ("Sheared LLaMA", "Cắt tỉa\nthông minh", ACADEMIA),
            ("ProLong", "512K\ncontext", HIGHLIGHT),
            ("SimPO", "Preference\nOptimization", SUCCESS),
        ]

        cards = VGroup()

        for n, d, c in specs:
            bg = RoundedRectangle(
                width=3.2,
                height=1.8,
                corner_radius=0.2,
                color=c,
                fill_color=c,
                fill_opacity=0.12,
            )

            nm = T(n, 20, c, weight=BOLD)
            ds = T(d, 15, WHITE)

            ds.next_to(nm, DOWN, buff=0.12)

            VGroup(nm, ds).move_to(bg)

            cards.add(VGroup(bg, nm, ds))

        cards.arrange(RIGHT, buff=0.35).shift(UP * 0.5)

        with self.voiceover(
            """
            Nếu nhìn lại toàn bộ hành trình Princeton NLP,
            chúng ta sẽ thấy rất nhiều dự án khác nhau.

            Sheared LLaMA.
            ProLong.
            SimPO.
            Và cả Goedel Prover.
            """
        ):
            self.play(
                LaggedStart(
                    *[FadeIn(c, shift=UP * 0.2) for c in cards],
                    lag_ratio=0.4,
                ),
                run_time=2,
            )

        msg = T(
            "Ít tài nguyên  →  Nhiều đổi mới",
            24,
            HIGHLIGHT,
            weight=BOLD,
        ).shift(DOWN * 1.5)

        with self.voiceover(
            """
            Nhưng phía sau tất cả những công trình này
            là một triết lý rất nhất quán.

            Không phải nhiều tài nguyên hơn.

            Mà là sử dụng tài nguyên thông minh hơn.
            """
        ):
            self.play(
                FadeIn(msg, shift=UP * 0.2),
                run_time=1,
            )

        final_line = T(
            "Sinh ra trong giới học thuật • Vươn tới SOTA",
            18,
            INDUSTRY,
            weight=BOLD,
        ).shift(DOWN * 2.5)

        badges = VGroup(*[
            sota_badge().scale(0.8).next_to(c, UP, buff=0.08)
            for c in cards
        ])

        with self.voiceover(
            """
            Chính điều đó đã giúp Princeton NLP nhiều lần
            tạo ra các kết quả đạt chuẩn trạng thái công nghệ tiên tiến nhất.

            Một minh chứng rằng:
            đổi mới thực sự không chỉ đến từ quy mô,
            mà còn đến từ ý tưởng đúng đắn.
            """
        ):
            self.play(
                LaggedStart(
                    *[FadeIn(b, scale=0.25) for b in badges],
                    lag_ratio=0.25,
                ),
                run_time=1,
            )

            flash_mob(self, badges, radius=1.8)

            self.play(
                FadeIn(final_line),
                run_time=0.7,
            )

            self.wait(2)

        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 — P5_Summary  (00:54 → 01:31)
# CSV rows 118–120  |  3 voiceovers
# ══════════════════════════════════════════════════════════════════════════════
class P5_Summary(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ── VO5 · row 118 (00:54–01:10)  ─────────────────────────────────────
        # Two-column: industry limitations vs. academia contributions (slide 53)
        hdr = T("VAI TRÒ CỦA HỌC THUẬT", 26, ACADEMIA, weight=BOLD).shift(UP * 2.7)

        # Left column — what academia doesn't have
        lft_title = T("Không có:", 17, INDUSTRY, weight=BOLD).shift(LEFT * 3.5 + UP * 1.6)
        lft_items = VGroup(
            T("✗  Siêu mô hình thương mại", 16, INDUSTRY),
            T("✗  Hàng nghìn GPU",           16, INDUSTRY),
            T("✗  Hàng tỉ USD ngân sách",    16, INDUSTRY),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(LEFT * 3.5 + UP * 0.5)

        divider = Line(UP * 2.0, DOWN * 2.0, color=NEUTRAL, stroke_width=1.8)

        # Right column — what academia contributes
        rgt_title = T("Đóng góp:", 17, SUCCESS, weight=BOLD).shift(RIGHT * 3.2 + UP * 1.6)
        rgt_items = VGroup(
            T("✓  Tri thức nền tảng quý giá", 16, SUCCESS),
            T("✓  Thực nghiệm có kiểm soát",  16, SUCCESS),
            T("✓  Bài báo khoa học chất lượng", 16, SUCCESS),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 3.0 + UP * 0.5)

        sub_note = T(
            "Đóng góp tri thức nền tảng quý giá cho nhân loại",
            15, NEUTRAL
        ).shift(DOWN * 2.2)

        with self.voiceover(
            "Giới học thuật có thể không sở hữu những siêu mô hình thương mại, nhưng "
            "chúng ta đang đóng góp những tri thức nền tảng quý giá cho nhân loại thông "
            "qua những thực nghiệm có kiểm soát chặt chẽ và những bài báo khoa học chất lượng."
        ):
            self.play(FadeIn(hdr, shift=DOWN * 0.1), run_time=0.45)
            self.play(Create(divider), run_time=0.4)
            self.play(
                FadeIn(lft_title, shift=RIGHT * 0.15),
                FadeIn(rgt_title, shift=LEFT * 0.15),
                run_time=0.5,
            )
            self.play(
                LaggedStart(*[FadeIn(it, shift=RIGHT * 0.2) for it in lft_items],
                            lag_ratio=0.35),
                run_time=1.4,
            )
            self.wait(1.5)
            self.play(
                LaggedStart(*[FadeIn(it, shift=LEFT * 0.2) for it in rgt_items],
                            lag_ratio=0.35),
                run_time=1.4,
            )
            self.wait(1.5)
            self.play(FadeIn(sub_note, shift=UP * 0.1), run_time=0.4)
            self.wait(1.5)

        clear(self)

        # ── VO6 · row 119 (01:10–01:21)  ─────────────────────────────────────
        # Three confirmed research directions as badge cards
        hdr3 = T("CÁC HƯỚNG ĐI ĐÃ KHẲNG ĐỊNH", 24, HIGHLIGHT, weight=BOLD).shift(UP * 2.7)
        period = T("vài năm qua", 14, NEUTRAL).next_to(hdr3, DOWN, buff=0.16)

        dir_data = [
            ("Mô hình ngôn ngữ\nquy mô nhỏ",     ACADEMIA,  "Small LMs"),
            ("Tinh lọc\ndữ liệu",                 HIGHLIGHT, "Data Curation"),
            ("Tinh chỉnh\nhậu huấn luyện",        SUCCESS,   "Post-Training"),
        ]
        dir_cards = VGroup()
        for label, col, eng in dir_data:
            outer = RoundedRectangle(corner_radius=0.25, width=3.2, height=2.0,
                                      color=col, fill_color=col, fill_opacity=0.12,
                                      stroke_width=2.5)
            check = T("✓", 32, col, weight=BOLD).move_to(outer.get_top() + DOWN * 0.45)
            main  = T(label, 16, WHITE)
            eng_l = T(eng,   14, col)
            eng_l.next_to(main, DOWN, buff=0.10)
            VGroup(main, eng_l).next_to(check, DOWN, buff=0.12)
            dir_cards.add(VGroup(outer, check, main, eng_l))
        dir_cards.arrange(RIGHT, buff=0.30).shift(DOWN * 0.05)

        with self.voiceover(
            "Các hướng đi như mô hình ngôn ngữ quy mô nhỏ, tinh lọc dữ liệu hay tinh "
            "chỉnh hậu huấn luyện đều đã khẳng định được chỗ đứng trong vài năm qua."
        ):
            self.play(FadeIn(hdr3, shift=DOWN * 0.1), FadeIn(period), run_time=0.45)
            self.play(
                LaggedStart(*[FadeIn(c, scale=0.6) for c in dir_cards], lag_ratio=0.30),
                run_time=1.8,
            )
            self.wait(1.5)
            self.play(
                LaggedStart(*[Indicate(c, scale_factor=1.06) for c in dir_cards],
                             lag_ratio=0.35),
                run_time=1.8,
            )
            self.wait(1.0)

        clear(self)

        # ── VO7 · row 120 (01:21–01:31)  ─────────────────────────────────────
        # Academia as a sanctuary for bold ideas — setup for next scene
        hdr4 = T("ĐIỀU TUYỆT VỜI NHẤT", 28, HIGHLIGHT, weight=BOLD).shift(UP * 2.7)

        # Expanding ring of ideas
        sanctuary = Circle(radius=1.8, color=ACADEMIA, stroke_width=2.0,
                           fill_color=ACADEMIA, fill_opacity=0.08)
        inner_txt = T("HỌC\nTHUẬT", 22, ACADEMIA, weight=BOLD).move_to(sanctuary)

        idea_words = ["Táo bạo", "Độc đáo", "Điên rồ", "Đột phá"]
        idea_mobs  = VGroup()
        for i, word in enumerate(idea_words):
            angle = PI / 2 + i * TAU / len(idea_words)
            pos   = 2.0 * np.array([np.cos(angle), np.sin(angle), 0])
            dot   = Dot(pos, color=HIGHLIGHT, radius=0.07)
            lbl   = T(word, 16, HIGHLIGHT, weight=BOLD)
            lbl.next_to(dot, direction=pos / np.linalg.norm(pos[:2].tolist() + [0]),
                        buff=0.15)
            ln    = DashedLine(sanctuary.point_at_angle(angle), dot.get_center(),
                               color=ACADEMIA, stroke_width=1.5, dash_length=0.12)
            idea_mobs.add(VGroup(ln, dot, lbl))

        tagline = T(
            "Dung dưỡng những ý tưởng táo bạo, độc đáo và điên rồ nhất",
            17, WHITE
        ).shift(DOWN * 2.7)

        with self.voiceover(
            "Nhưng điều tuyệt vời nhất ở trường đại học không dừng lại ở đó, mà nằm ở "
            "việc: Nơi đây luôn dung dưỡng và khuyến khích những ý tưởng táo bạo, độc "
            "đáo và điên rồ nhất."
        ):
            self.play(FadeIn(hdr4, shift=DOWN * 0.1), run_time=0.45)
            self.play(Create(sanctuary), FadeIn(inner_txt, scale=0.5), run_time=0.8)
            self.play(
                LaggedStart(*[FadeIn(im, scale=0.5) for im in idea_mobs], lag_ratio=0.45),
                run_time=2.0,
            )
            self.play(FadeIn(tagline, shift=UP * 0.12), run_time=0.5)
            self.wait(1.0)

        self.wait(0.4)
        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 — P5_BoldIdeas  (01:31 → 02:22)
# CSV rows 121–126  |  6 voiceovers
# ══════════════════════════════════════════════════════════════════════════════
class P5_BoldIdeas(VoiceoverScene):
    """
    Cải tiến:
    - Các câu hỏi học thuật tự động trôi nổi, dập dềnh động đậy sống động bằng Updaters.
    - Phóng to khối Transformer tạo điểm nhấn điện ảnh rõ ràng.
    - Căn chỉnh hoàn hảo khoảng cách phần Thử thách giả định chống đè layout.
    """

    def construct(self):
        self.set_speech_service(svc())

        # =====================================================================
        # VO8 — INTRO + TRANSFORMER QUESTION (Đã phóng to hộp Transformer)
        # =====================================================================
        intro = T(
            "NHỮNG Ý TƯỞNG TÁO BẠO",
            32,
            HIGHLIGHT,
            weight=BOLD,
        )

        subtitle = T(
            "Nơi những giả định nền tảng bị đặt dấu hỏi",
            18,
            NEUTRAL,
        ).next_to(intro, DOWN)

        with self.voiceover(
                """
                Và chính từ môi trường học thuật ấy,
                những câu hỏi táo bạo nhất bắt đầu xuất hiện.
                Không phải cách cải tiến thêm vài phần trăm,
                mà là đặt lại câu hỏi từ chính nền móng.
                """
        ):
            self.play(Write(intro), run_time=1.2)
            self.play(FadeIn(subtitle), run_time=0.8)
            self.wait(1.5)

        self.play(
            FadeOut(intro),
            FadeOut(subtitle),
            run_time=0.6,
        )

        # PHÓNG TO KHỐI TRANSFORMER ĐỂ TẠO SỰ NỔI BẬT KHÔNG GIAN
        transformer = RoundedRectangle(
            corner_radius=0.25,
            width=5.5,  # Tăng từ 4.2 lên 5.5
            height=1.5,  # Tăng từ 1.2 lên 1.5
            color=ACADEMIA,
            fill_opacity=0.12,
            stroke_width=3
        )

        trans_txt = T(
            "Transformer",
            32,  # Tăng font size từ 26 lên 32
            ACADEMIA,
            weight=BOLD,
        ).move_to(transformer)

        trans_group = VGroup(transformer, trans_txt).shift(LEFT * 0.8)

        qmark = T(
            "?",
            150,
            HIGHLIGHT,
            weight=BOLD,
        ).shift(RIGHT * 3.5)

        with self.voiceover(
                """
                Ví dụ như một câu hỏi tưởng chừng điên rồ:
                Điều gì sẽ xảy ra nếu thế hệ AI tiếp theo
                không còn sử dụng kiến trúc Transformer?
                """
        ):
            self.play(FadeIn(trans_group, scale=0.7), run_time=0.8)
            self.wait(0.8)

            self.play(
                trans_group.animate.scale(1.05),
                Flash(transformer, color=ACADEMIA, flash_radius=1.0),
                run_time=0.7,
            )
            self.wait(0.6)

            self.play(
                FadeIn(qmark, shift=LEFT * 0.2),
                run_time=0.8,
            )
            self.wait(1.5)

        self.play(
            FadeOut(trans_group),
            FadeOut(qmark),
            run_time=0.5,
        )

        # =====================================================================
        # VO9 — QUESTION FOUNDATIONS (Căn chỉnh lại khoảng cách an toàn)
        # =====================================================================
        hdr = T(
            "THỬ THÁCH CÁC GIẢ ĐỊNH NỀN TẢNG",
            24,
            HIGHLIGHT,
            weight=BOLD,
        ).to_edge(UP, buff=0.4)

        # Đẩy dịch sang trái (LEFT * 3.8) để chừa khoảng không rộng rãi ở giữa
        ntp = mk_rbox(
            "Next Token\nPrediction",
            3.2,
            1.1,
            INDUSTRY,
            fs=18,
        ).shift(LEFT * 3.8 + UP * 0.6)

        webdata = mk_rbox(
            "Web Data\nKhổng Lồ",
            3.2,
            1.1,
            INDUSTRY,
            fs=18,
        ).shift(LEFT * 3.8 + DOWN * 1.4)

        cross1 = Cross(ntp, stroke_color=INDUSTRY, stroke_width=4)
        cross2 = Cross(webdata, stroke_color=INDUSTRY, stroke_width=4)

        synth = mk_rbox(
            "Synthetic Data\nChất Lượng Cao",
            3.6,
            1.3,
            SUCCESS,
            fs=18,
        ).shift(RIGHT * 3.2 + DOWN * 0.4)

        # Trục mũi tên ngắn gọn, vuông vắn không chạm biên khối rbox
        arr = Arrow(
            LEFT * 1.2,
            RIGHT * 0.8,
            color=HIGHLIGHT,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        ).shift(DOWN * 0.4)

        with self.voiceover(
                """
                Biết đâu chúng ta cũng không cần xem
                dự đoán token tiếp theo là mục tiêu lớn.
    
                Biết đâu tương lai không nằm ở việc thu thập
                thêm hàng nghìn tỷ token từ Internet,
                mà nằm ở dữ liệu tổng hợp có chất lượng vượt trội.
                """
        ):
            self.play(FadeIn(hdr), run_time=0.4)

            self.play(FadeIn(ntp), run_time=0.6)
            self.play(Create(cross1), run_time=0.4)
            self.wait(3)

            self.play(FadeIn(webdata), run_time=0.6)
            self.play(Create(cross2), run_time=0.4)
            self.wait(3.5)

            self.play(Create(arr), run_time=0.5)

            self.play(
                FadeIn(synth, scale=0.8),
                Flash(synth, color=SUCCESS, flash_radius=1.1),
                run_time=0.8,
            )
            self.wait(1.5)

        clear(self)

        # =====================================================================
        # VO10 — ACADEMIA TEMPLE (Floating nodes không giật)
        # =====================================================================

        temple_circle = Circle(
            radius=1.6,
            color=ACADEMIA,
            fill_opacity=0.08,
            stroke_width=3
        )

        temple_txt = T(
            "HỌC THUẬT",
            32,
            ACADEMIA,
            weight=BOLD,
        )

        ideas = [
            "Why?",
            "What if?",
            "Impossible?",
            "Alternative?",
        ]

        idea_nodes = VGroup()

        for i, txt in enumerate(ideas):
            ang = i * TAU / 4 + PI / 4

            base_pos = 2.8 * np.array([
                np.cos(ang),
                np.sin(ang),
                0
            ])

            # --------------------------------------------------
            # DOT
            # --------------------------------------------------

            dot = Dot(
                point=base_pos,
                color=HIGHLIGHT,
                radius=0.09
            )

            dot.base_pos = base_pos
            dot.phase = i * 1.7

            # --------------------------------------------------
            # LABEL
            # --------------------------------------------------

            direction = UP if base_pos[1] < 0 else DOWN

            lbl = T(
                txt,
                16,
                HIGHLIGHT
            )

            lbl.next_to(
                dot,
                direction,
                buff=0.15
            )

            # --------------------------------------------------
            # LABEL FOLLOW DOT
            # --------------------------------------------------

            def make_label_updater(target_dot, direction):
                def updater(m):
                    m.next_to(
                        target_dot,
                        direction,
                        buff=0.15
                    )

                return updater

            lbl.add_updater(
                make_label_updater(dot, direction)
            )

            # --------------------------------------------------
            # FLOATING DOT
            # --------------------------------------------------

            def make_dot_updater(phase):
                t = phase

                def updater(mob, dt):
                    nonlocal t

                    t += dt * 1.2

                    offset = np.array([
                        0.12 * np.sin(t),
                        0.08 * np.cos(t * 1.4),
                        0
                    ])

                    mob.move_to(
                        mob.base_pos + offset
                    )

                return updater

            dot.add_updater(
                make_dot_updater(dot.phase)
            )

            node = VGroup(dot, lbl)

            idea_nodes.add(node)

        # =====================================================================
        # ANIMATION
        # =====================================================================

        with self.voiceover(
                """
                Và đó chính là lý do học thuật đặc biệt.
                Đây là nơi người ta được phép đặt ra
                những câu hỏi có khả năng lật đổ toàn bộ hiện trạng.
                """
        ):

            self.play(
                Create(temple_circle),
                FadeIn(temple_txt, scale=0.8),
                run_time=1.0,
            )

            self.play(
                LaggedStart(
                    *[
                        FadeIn(node, scale=0.5)
                        for node in idea_nodes
                    ],
                    lag_ratio=0.2,
                ),
                run_time=1.5,
            )

            self.wait(2.2)

        # =====================================================================
        # CLEANUP
        # =====================================================================

        for node in idea_nodes:
            node[0].clear_updaters()  # dot
            node[1].clear_updaters()  # label

        clear(self)
        # =====================================================================
        # VO11 — SCALE PARADOX
        # =====================================================================
        hdr2 = T(
            "NGHỊCH LÝ CỦA HỌC THUẬT",
            28,
            INDUSTRY,
            weight=BOLD,
        ).to_edge(UP)

        idea_box = mk_rbox(
            "Ý tưởng\nđột phá",
            3,
            1.2,
            ACADEMIA,
            fs=20,
        ).shift(LEFT * 4)

        scale_wall = Rectangle(
            width=0.5,
            height=4,
            color=INDUSTRY,
            fill_color=INDUSTRY,
            fill_opacity=0.8,
        )

        wall_txt = T(
            "SCALE",
            20,
            WHITE,
            weight=BOLD,
        ).rotate(PI / 2).move_to(scale_wall)

        validation = mk_rbox(
            "Kiểm chứng\nquy mô lớn",
            3,
            1.2,
            SUCCESS,
            fs=20,
        ).shift(RIGHT * 4)

        idea_dot = Dot(
            idea_box.get_right(),
            color=ACADEMIA,
            radius=0.12,
        )

        path = Line(
            idea_box.get_right(),
            scale_wall.get_left(),
            color=ACADEMIA,
        )

        with self.voiceover(
                """
                Nhưng rồi một nghịch lý xuất hiện.
    
                Học thuật thường là nơi sinh ra ý tưởng.
                Tuy nhiên, lại không đủ nguồn lực
                để kiểm chứng chúng ở quy mô thật sự lớn.
                """
        ):
            self.play(
                FadeIn(hdr2),
                FadeIn(idea_box),
                run_time=0.8,
            )
            self.wait(1)

            self.play(
                FadeIn(scale_wall),
                FadeIn(wall_txt),
                run_time=0.5,
            )
            self.play(
                MoveAlongPath(idea_dot, path),
                run_time=1.2,
            )


            self.play(
                idea_dot.animate.shift(LEFT * 0.4),
                Flash(scale_wall, color=INDUSTRY),
                run_time=0.8,
            )
            self.wait(0.8)

            self.play(
                FadeIn(validation),
                run_time=0.6,
            )
            self.wait(1.5)

        clear(self)

        # =====================================================================
        # VO12 — MINH CHỨNG (EMNLP 2022)
        # =====================================================================
        mem_hdr = T("MINH CHỨNG: MÔ HÌNH BỘ NHỚ TĂNG CƯỜNG", 20, ACADEMIA, weight=BOLD).shift(UP * 2.7)
        ref_mem = T("Zhong et al., EMNLP 2022  ·  Princeton", 14, NEUTRAL).next_to(mem_hdr, DOWN, buff=0.15)

        base_y = -1.7
        ind_h = 3.2
        mem_h = 0.85
        ind_cx = -2.0
        mem_cx = 2.0
        bar_w = 1.2

        base_line = Line(LEFT * 4.0 + UP * base_y, RIGHT * 4.0 + UP * base_y, color=NEUTRAL, stroke_width=1.5)

        ind_bar = Rectangle(width=bar_w, height=ind_h, color=INDUSTRY, fill_color=INDUSTRY, fill_opacity=0.65)
        ind_bar.move_to(np.array([ind_cx, base_y + ind_h / 2, 0]))
        ind_top_lbl = T("Công nghiệp", 15, INDUSTRY, weight=BOLD).next_to(ind_bar, UP, buff=0.1)
        ind_bot_lbl = T("~Nghìn tỉ\ntham số", 14, NEUTRAL).move_to(np.array([ind_cx, base_y - 0.42, 0]))

        mem_bar = Rectangle(width=bar_w, height=mem_h, color=ACADEMIA, fill_color=ACADEMIA, fill_opacity=0.75)
        mem_bar.move_to(np.array([mem_cx, base_y + mem_h / 2, 0]))
        mem_bot_lbl = T("Bộ nhớ tăng cường\n~200M tham số", 14, ACADEMIA).move_to(np.array([mem_cx, base_y - 0.45, 0]))

        ceil_y = base_y + mem_h
        ceiling = DashedLine(np.array([mem_cx - 0.8, ceil_y, 0]), np.array([mem_cx + 2.1, ceil_y, 0]), color=HIGHLIGHT,
                             stroke_width=2.8, dash_length=0.13)
        ceil_lbl = T("✗  Hết kinh phí!", 14, HIGHLIGHT, weight=BOLD).move_to(np.array([mem_cx + 1.5, ceil_y + 0.32, 0]))

        sad_note = T("Ý tưởng hay chưa bao giờ có cơ hội được lớn lên", 15, INDUSTRY).shift(DOWN * 2.6)

        with self.voiceover(
                "Câu chuyện về mô hình bộ nhớ tăng cường chỉ dừng lại ở quy mô 200 triệu "
                "tham số cách đây 3 năm vì thiếu kinh phí chính là một minh chứng đau lòng "
                "cho những ý tưởng hay chưa bao giờ có cơ hội được lớn lên."
        ):
            self.play(FadeIn(mem_hdr, shift=DOWN * 0.1), FadeIn(ref_mem), run_time=0.45)
            self.wait(1.0)
            self.play(Create(base_line), run_time=0.3)
            self.wait(0.5)
            self.play(GrowFromEdge(ind_bar, DOWN), run_time=1.5)
            self.play(FadeIn(ind_top_lbl), FadeIn(ind_bot_lbl), run_time=0.5)
            self.wait(1.5)
            self.play(GrowFromEdge(mem_bar, DOWN), run_time=1.2)
            self.play(FadeIn(mem_bot_lbl), run_time=0.4)
            self.wait(1.0)
            self.play(Create(ceiling), FadeIn(ceil_lbl), run_time=0.55)
            self.wait(2.0)
            self.play(FadeIn(sad_note, shift=UP * 0.1), run_time=0.45)
            self.wait(2.5)
            self.play(Indicate(ceiling, color=INDUSTRY), run_time=0.8)
            self.wait(1.5)

        clear(self)

        # =====================================================================
        # VO13 — CLIFFHANGER
        # =====================================================================
        gpu_icons = VGroup()

        for i in range(8):
            gpu = RoundedRectangle(
                corner_radius=0.1,
                width=0.8,
                height=0.6,
                color=NEUTRAL,
            )
            gpu_icons.add(gpu)

        gpu_icons.arrange(RIGHT, buff=0.15)

        missing = VGroup(*gpu_icons[4:])

        crosses = VGroup(*[
            Cross(g, stroke_color=INDUSTRY)
            for g in missing
        ])

        question_box = RoundedRectangle(
            corner_radius=0.25,
            width=9.2,
            height=1.8,
            color=HIGHLIGHT,
            fill_opacity=0.08,
        ).shift(DOWN * 1.8)

        question_txt = T(
            "Nếu một phòng lab còn không có nổi 4–8 GPU,\n"
            "thì lối thoát thực sự là gì?",
            24,
            WHITE,
            weight=BOLD,
        ).move_to(question_box)

        with self.voiceover(
                """
                Và khi một phòng thí nghiệm
                thậm chí còn không sở hữu nổi vài GPU cơ bản,
    
                câu hỏi quan trọng nhất không còn là
                chúng ta muốn làm gì.
    
                Mà là:
                chúng ta phải hợp tác như thế nào.
                """
        ):
            self.play(FadeIn(gpu_icons), run_time=0.7)
            self.play(
                LaggedStart(*[FadeIn(c) for c in crosses], lag_ratio=0.15),
                run_time=0.8,
            )
            self.wait(1)

            self.play(
                Create(question_box),
                FadeIn(question_txt),
                run_time=0.8,
            )
            self.wait(2.5)

        clear(self)


# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 — P5_Collaboration  (02:17 → 02:52)
# CSV rows 127–130  |  4 voiceovers
# ══════════════════════════════════════════════════════════════════════════════
class P5_Collaboration(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ==========================================================
        # VO14: MẠNG LƯỚI TẬP TRUNG (Sửa triệt để lỗi xuyên hình tròn)
        # ==========================================================
        hdr = T("LỐI THOÁT KHÔNG NẰM Ở NHIỀU GPU HƠN", 26, HIGHLIGHT, weight=BOLD).shift(UP * 2.8)
        sub_hdr = T("Mà nằm ở cách chúng ta kết nối nguồn lực", 16, NEUTRAL).next_to(hdr, DOWN, buff=0.15)
        network_title = T("Kết nối thành một mạng lưới chung", 18, SUCCESS, weight=BOLD).shift(UP * 1.5)

        # Định vị khối trung tâm chính xác
        center_circle = Circle(radius=0.8, color=SUCCESS, fill_color=SUCCESS, fill_opacity=0.2, stroke_width=3)
        center_text = T("Shared\nCompute", 14, SUCCESS, weight=BOLD)
        center = VGroup(center_circle, center_text).shift(DOWN * 0.4)
        center_text.move_to(center_circle.get_center())

        labs = VGroup()
        gpu_icons = VGroup()
        network_edges = VGroup()

        offsets = [
            LEFT * 4.2 + UP * 0.7,  # Lab 1
            RIGHT * 4.2 + UP * 0.7,  # Lab 2
            LEFT * 4.2 + DOWN * 1.3,  # Lab 3
            RIGHT * 4.2 + DOWN * 1.3,  # Lab 4
        ]

        for i, offset in enumerate(offsets):
            pos = center_circle.get_center() + offset

            c = Circle(radius=0.5, color=INDUSTRY, fill_color=INDUSTRY, fill_opacity=0.15, stroke_width=2)
            txt = T(f"Lab {i + 1}", 14, INDUSTRY, weight=BOLD)
            lab = VGroup(c, txt).move_to(pos)
            txt.move_to(c.get_center())
            labs.add(lab)

            gpu = T("GPU", 11, NEUTRAL).next_to(lab, DOWN, buff=0.1)
            gpu_icons.add(gpu)

            # ── CÁCH SỬA TUYỆT ĐỐI CHỐNG ĐÈ: TÍNH TOÁN VỊ TRÍ ĐẦU VÀ CUỐI CỦA LINE ──
            # Lấy vectơ hướng từ tâm Lab đến tâm Shared Compute
            start_p = c.get_center()
            end_p = center_circle.get_center()
            vec = end_p - start_p
            unit_vec = vec / np.linalg.norm(vec)  # Vectơ đơn vị

            # Điểm bắt đầu lùi vào sát viền Lab (cách tâm Lab một khoảng bằng bán kính 0.5)
            edge_start = start_p + unit_vec * 0.5
            # Điểm kết thúc dừng ngay viền Center (cách tâm Center một khoảng bằng bán kính 0.8)
            edge_end = end_p - unit_vec * 0.8

            # Vẽ đường thẳng đi từ viền này đến viền kia, hoàn toàn không chạm chữ
            edge = Line(
                edge_start,
                edge_end,
                color=SUCCESS,
                stroke_width=2
            ).set_opacity(0.55).set_z_index(-1)

            network_edges.add(edge)

        subtitle = T("Từ cạnh tranh tài nguyên  →  phối hợp tài nguyên", 16, HIGHLIGHT, weight=BOLD).to_edge(DOWN,
                                                                                                             buff=0.4)

        # ============================================================
        # VOICEOVER & ANIMATION (Đã tinh chỉnh nhịp điệu timeline xuất hiện)
        # ============================================================

        with self.voiceover(
                """
                Có lẽ lối thoát không nằm ở việc sở hữu nhiều GPU hơn.
                Mà nằm ở việc chúng ta thay đổi cách phối hợp với nhau.
                Nếu kết nối toàn bộ các phòng thí nghiệm lại thành một mạng lưới chung,
                tổng năng lực nghiên cứu có thể lớn hơn rất nhiều so với từng đơn vị hoạt động đơn lẻ.
                """
        ):
            # 1. VÀO CẢNH: Xuất hiện tiêu đề chính cùng toàn bộ các Lab vệ tinh ngay lập tức
            self.play(
                FadeIn(hdr, shift=DOWN * 0.15),
                FadeIn(sub_hdr),
                run_time=0.8,
            )
            self.play(
                LaggedStart(*[FadeIn(lab, scale=0.8) for lab in labs], lag_ratio=0.1),
                LightningStart=LaggedStart(*[FadeIn(g) for g in gpu_icons], lag_ratio=0.08),
                run_time=1.0
            )

            # 2. ĐOẠN NGHỈ: Giữ nguyên trạng thái các Lab độc lập trong lúc đọc câu đầu tiên (khoảng 1.2 giây)
            self.wait(5)

            # 3. KHI NÓI ĐẾN "Mà nằm ở việc... kết nối thành mạng lưới chung":
            # Xuất hiện Shared Compute và Tiêu đề mạng lưới cùng một lúc để tạo điểm nhấn tư duy mới
            self.play(
                FadeIn(center, scale=0.7),
                run_time=0.85,
            )
            self.wait(2)

            # 4. KẾT NỐI MẠNG LƯỚI: Các đường line chạy từ vệ tinh tụ về lõi xử lý trung tâm
            self.play(
                FadeIn(network_title, shift=UP * 0.1),
                LaggedStart(*[Create(edge) for edge in network_edges], lag_ratio=0.12),
                run_time=1.2,
            )

            # Hiệu ứng phát sáng báo hiệu mạng lưới kích hoạt thành công
            self.play(
                Flash(center_circle, color=SUCCESS, flash_radius=0.9, run_time=0.6)
            )

            # 5. KẾT LUẬN: Xuất hiện dòng chữ chuyển đổi tư duy ở dưới đáy màn hình
            self.play(
                FadeIn(subtitle),
                run_time=0.5,
            )

            # Chờ đọc nốt câu cuối cùng của đoạn voiceover trước khi clear cảnh
            self.wait(1.8)

        clear(self)

        # ==========================================================
        # VO15: CLUSTER SHARING (Đồng bộ xuất hiện mũi tên + dịch chuyển)
        # ==========================================================
        hdr2 = T("CLUSTER SHARING", 26, ACADEMIA, weight=BOLD).shift(UP * 2.8)
        ref = T("Princeton REAPER Scheduler", 16, NEUTRAL).next_to(hdr2, DOWN, buff=0.2)

        labA = mk_rbox("Lab A\n(GPU nhàn rỗi)", 2.4, 1, SUCCESS).shift(LEFT * 4.3 + UP * 0.1)
        scheduler = mk_rbox("REAPER\nScheduler", 2.6, 1.1, HIGHLIGHT).shift(UP * 0.1)
        labB = mk_rbox("Lab B\n(Đang chờ GPU)", 2.4, 1, INDUSTRY).shift(RIGHT * 4.3 + UP * 0.1)

        # Khai báo mũi tên động động (Chỉ xuất hiện khi có lệnh gọi cụ thể)
        arrow_to_sched = Arrow(labA.get_right(), scheduler.get_left(), color=NEUTRAL, stroke_width=3, buff=0.1, max_tip_length_to_length_ratio=0.12)
        arrow_from_sched = Arrow(scheduler.get_right(), labB.get_left(), color=NEUTRAL, stroke_width=3, buff=0.1, max_tip_length_to_length_ratio=0.12)

        gpu_tokens = VGroup(*[
            Square(side_length=0.16, color=SUCCESS, fill_opacity=1, stroke_width=1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.05).next_to(labA, DOWN, buff=0.25)

        with self.voiceover(
                """
                Một ví dụ rất thú vị đến từ Princeton.
                Thay vì để GPU nhàn rỗi ở phòng thí nghiệm này trong khi phòng khác đang phải xếp hàng chờ,
                bộ lập lịch Reaper sẽ tự động điều phối tài nguyên trên toàn cụm máy tính.
                """
        ):
            self.play(FadeIn(hdr2), FadeIn(ref), run_time=0.7)
            self.play(FadeIn(labA), FadeIn(labB), FadeIn(scheduler), run_time=0.8)
            self.wait(2)
            self.play(FadeIn(gpu_tokens, shift=UP * 0.15))
            self.wait(4)  # Chờ đến đoạn thoại "Thay vì để GPU nhàn rỗi..."

            # TIMELINE MỚI: Mũi tên 1 vẽ ra -> Đồng thời Token di chuyển theo mũi tên vào bộ lập lịch
            self.play(
                Create(arrow_to_sched),
                gpu_tokens.animate.move_to(scheduler.get_bottom() + DOWN * 0.4),
                run_time=1,
                rate_func=smooth
            )
            self.play(Indicate(scheduler, color=HIGHLIGHT, scale_factor=1.05), run_time=0.4)

            # Mũi tên 2 vẽ ra -> Đồng thời Token chuyển màu cảnh báo và bay sang cấp phát cho Lab B
            self.play(
                Create(arrow_from_sched),
                gpu_tokens.animate.move_to(labB.get_bottom() + DOWN * 0.4).set_color(HIGHLIGHT),
                run_time=1,
                rate_func=smooth
            )
            self.wait(2.0)

        clear(self)

        # ==========================================================
        # VO16: GPU POOL QUỐC GIA (HIỆU ỨNG CHẠM VIỀN BIẾN MẤT)
        # ==========================================================
        hdr3 = T("GPU POOL QUỐC GIA", 26, SUCCESS, weight=BOLD).shift(UP * 2.8)
        subtitle3 = T("Châu Âu & Canada", 16, NEUTRAL).next_to(hdr3, DOWN, buff=0.2)

        center_pool = Circle(radius=0.85, color=SUCCESS, fill_opacity=0.2, stroke_width=3).shift(DOWN * 0.8)
        pool_text = T("GPU\nPOOL", 18, SUCCESS, weight=BOLD).move_to(center_pool)

        unis = VGroup()
        gathering_targets = []  # Lưu các điểm chạm trên viền khi GOM
        distributing_starts = []  # Lưu các điểm xuất phát trên viền khi PHÂN PHỐI

        for i in range(5):
            angle = i * TAU / 5 - PI / 2
            pos = center_pool.get_center() + np.array([2.1 * np.cos(angle), 2.1 * np.sin(angle), 0])

            node = Circle(radius=0.35, color=ACADEMIA, fill_opacity=0.15, stroke_width=2).move_to(pos)
            label = T(f"U{i + 1}", 13, ACADEMIA, weight=BOLD).move_to(node)
            unis.add(VGroup(node, label))

            # ── TÍNH TOÁN VECTOR ĐIỂM CHẠM TRÊN VIỀN ──
            # Vectơ đơn vị hướng từ tâm Pool ra tâm của Trường U(i)
            vec = node.get_center() - center_pool.get_center()
            unit_vec = vec / np.linalg.norm(vec)

            # Điểm nằm ngay trên đường viền của center_pool (bán kính 0.85)
            border_point = center_pool.get_center() + unit_vec * 0.85

            gathering_targets.append(border_point)
            distributing_starts.append(border_point)

        # 1. Khởi tạo mảng chấm dùng cho hành động GOM (Xuất phát từ tâm các trường)
        gathering_dots = VGroup(*[
            Dot(u[0].get_center(), color=HIGHLIGHT, radius=0.08)
            for u in unis
        ])

        # 2. Khởi tạo mảng chấm dùng cho hành động PHÂN PHỐI (Xuất phát ngay từ viền vòng tròn lớn)
        distributing_dots = VGroup(*[
            Dot(start_p, color=SUCCESS, radius=0.08)
            for start_p in distributing_starts
        ])

        with self.voiceover(
                """
                Một hướng đi xa hơn đang được nhiều quốc gia áp dụng.
                Nguồn lực GPU được gom về một trung tâm dùng chung,
                từ đó phân phối lại theo nhu cầu nghiên cứu thực tế.
                """
        ):
            # CÂU 1: Dựng bối cảnh nền tảng
            self.play(FadeIn(hdr3), FadeIn(subtitle3), run_time=0.6)
            self.play(Create(center_pool), FadeIn(pool_text), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(u, scale=0.8) for u in unis], lag_ratio=0.1), run_time=0.8)
            self.wait(2.4)

            # CÂU 2: "Nguồn lực GPU được gom về một trung tâm dùng chung,"
            self.play(FadeIn(gathering_dots, scale=0.5), run_time=0.3)

            # ANIMATION GOM: Chấm di chuyển đến ĐƯỜNG VIỀN (gathering_targets) thay vì vào tâm
            self.play(
                LaggedStart(*[
                    dot.animate.move_to(target)
                    for dot, target in zip(gathering_dots, gathering_targets)
                ], lag_ratio=0.1),
                run_time=1.2,
                rate_func=ease_in_quad
            )

            # Biến mất ngay lập tức khi chạm viền kèm hiệu ứng nổ nhẹ (Flash) giải phóng năng lượng vào kho
            self.play(
                FadeOut(gathering_dots),
                Flash(center_pool, color=HIGHLIGHT, num_lines=12, flash_radius=0.9),
                run_time=0.4
            )

            self.wait(1)

            # CÂU 3: "từ đó phân phối lại theo nhu cầu nghiên cứu thực tế."
            # ANIMATION PHÂN PHỐI: Xuất hiện từ viền đường tròn và bay về phía các trường
            self.play(FadeIn(distributing_dots, scale=0.5), run_time=0.2)
            self.play(
                LaggedStart(*[
                    dot.animate.move_to(u[0].get_center())
                    for dot, u in zip(distributing_dots, unis)
                ], lag_ratio=0.1),
                run_time=1.3,
                rate_func=ease_out_quad
            )

            # Kích hoạt hiệu ứng thành công tại từng node trường đại học
            self.play(
                FadeOut(distributing_dots),
                *[Flash(u[0], color=SUCCESS, flash_radius=0.5, num_lines=6) for u in unis],
                run_time=0.5
            )
            self.wait(1.0)

        clear(self)
        # ==========================================================
        # VO17: HỌC THUẬT ✕ CÔNG NGHIỆP (HỆ THỐNG LUỒNG ĐỐI XỨNG TOÀN DIỆN)
        # ==========================================================
        hdr4 = T("HỌC THUẬT ✕ CÔNG NGHIỆP", 26, HIGHLIGHT, weight=BOLD).shift(UP * 2.8)

        # Căn chỉnh vị trí các khối để chừa khoảng trống cho hệ thống "ống dẫn" bẻ góc
        industry = mk_rbox("Industry (Doanh nghiệp)", 3.4, 0.75, INDUSTRY, fs=16).shift(UP * 1.3)

        support_group = VGroup(
            mk_rbox("GPU Grants", 2.3, 0.6, SUCCESS, fs=13),
            mk_rbox("Cloud Credits", 2.3, 0.6, SUCCESS, fs=13),
            mk_rbox("Research Funding", 2.3, 0.6, SUCCESS, fs=13),
        ).arrange(RIGHT, buff=0.4).shift(DOWN * 0.1)

        academia = mk_rbox("Academia (Viện / Trường)", 3.4, 0.75, ACADEMIA, fs=16).shift(DOWN * 1.6)

        # ── THIẾT KẾ HỆ THỐNG MŨI TÊN "ỐNG DẪN" CHUẨN CHIẾN LƯỢC ──

        # 1. HỆ THỐNG PHÂN PHỐI (PHẦN TRÊN)
        top_piping = VGroup()
        y_split_top = (industry.get_bottom()[1] + support_group.get_top()[1]) / 2

        # Đường trục chính đi xuống từ Industry
        main_stem_top = Line(industry.get_bottom(), [0, y_split_top, 0], color=NEUTRAL, stroke_width=2.5)
        # Đường ngang phân phối
        horizontal_bar_top = Line(
            [support_group[0].get_center()[0], y_split_top, 0],
            [support_group[2].get_center()[0], y_split_top, 0],
            color=NEUTRAL, stroke_width=2.5
        )
        top_piping.add(main_stem_top, horizontal_bar_top)

        # 3 mũi tên hạ xuống support
        top_arrows = VGroup()
        for s in support_group:
            start_p = [s.get_center()[0], y_split_top, 0]
            arrow = Arrow(
                start=start_p, end=s.get_top(), buff=0.05,
                color=NEUTRAL, stroke_width=2.5, max_tip_length_to_length_ratio=0.15
            )
            top_arrows.add(arrow)

        # 2. HỆ THỐNG HỘI TỤ (PHẦN DƯỚI)
        bottom_piping = VGroup()
        y_split_bottom = (support_group.get_bottom()[1] + academia.get_top()[1]) / 2

        # 3 đường đi xuống từ đáy các ô support
        for s in support_group:
            line = Line(s.get_bottom(), [s.get_center()[0], y_split_bottom, 0], color=NEUTRAL, stroke_width=2.5)
            bottom_piping.add(line)

        # Đường ngang hội tụ
        horizontal_bar_bottom = Line(
            [support_group[0].get_center()[0], y_split_bottom, 0],
            [support_group[2].get_center()[0], y_split_bottom, 0],
            color=NEUTRAL, stroke_width=2.5
        )
        bottom_piping.add(horizontal_bar_bottom)

        # Mũi tên cuối cùng hội tụ vào Academia
        final_arrow = Arrow(
            start=[0, y_split_bottom, 0], end=academia.get_top(), buff=0.05,
            color=NEUTRAL, stroke_width=2.5, max_tip_length_to_length_ratio=0.15
        )

        final_text = T("Thu hẹp khoảng cách thế kỷ", 18, HIGHLIGHT, weight=BOLD).to_edge(DOWN, buff=0.3)

        # ============================================================
        # VOICE & ANIMATION (Timeline đã được tối ưu)
        # ============================================================
        with self.voiceover(
                """
                Và cuối cùng, khoảng cách giữa học thuật và công nghiệp cũng đang dần được thu hẹp.
                Thông qua các chương trình tài trợ nghiên cứu, tín dụng điện toán đám mây, hay các gói GPU hỗ trợ học thuật,
                nhiều ý tưởng từng bất khả thi nay đã có cơ hội được kiểm chứng.
                """
        ):
            self.play(FadeIn(hdr4), run_time=0.6)
            self.play(FadeIn(industry, shift=DOWN * 0.2), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(x, scale=0.9) for x in support_group], lag_ratio=0.15), run_time=0.9)
            self.play(FadeIn(academia, shift=UP * 0.2), run_time=0.7)

            # Vẽ hệ thống phân phối (Top)
            self.play(Create(main_stem_top), Create(horizontal_bar_top), run_time=0.6)
            self.play(LaggedStart(*[Create(a) for a in top_arrows], lag_ratio=0.1), run_time=0.8)

            # Vẽ hệ thống hội tụ (Bottom) - Kết nối các ô ngoài vào trung tâm
            self.play(Create(bottom_piping), run_time=0.6)
            self.play(Create(final_arrow), run_time=0.7)

            self.wait(0.3)
            self.play(FadeIn(final_text, shift=UP * 0.1), run_time=0.6)
            self.wait(2.5)

        clear(self)

# ══════════════════════════════════════════════════════════════════════════════
# Scene 5 — P5_CallToAction  (02:52 → 03:30)
# CSV rows 131–133  |  3 voiceovers
# ══════════════════════════════════════════════════════════════════════════════
class P5_CallToAction(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())

        # ==========================================================
        # VO18 (02:52–03:04) — SMALL EFFORTS → COMMUNITY
        # (Cải tiến: Lan tỏa mạng lưới phân cấp chống đè chữ)
        # ==========================================================
        title = T(
            "KHÔNG MỘT PHÒNG LAB NÀO XÂY DỰNG TƯƠNG LAI AI MỘT MÌNH",
            20,  # Thu nhỏ cỡ chữ một chút để bao quát toàn màn hình
            HIGHLIGHT,
            weight=BOLD,
        ).to_edge(UP, buff=0.4)

        # Đẩy tâm mạng lưới xuống thấp để chừa không gian trống rộng rãi
        center = Dot(radius=0.09, color=ACADEMIA).shift(DOWN * 0.4)

        with self.voiceover(
                """
                Sau tất cả những câu chuyện vừa rồi,
                có lẽ câu hỏi quan trọng nhất không còn là ai sở hữu nhiều GPU hơn.
                Mà là liệu chúng ta có thể kết nối những nỗ lực nhỏ bé ấy lại với nhau hay không.
                """
        ):
            # Xuất hiện tiêu đề và hạt nhân đầu tiên
            self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(center), run_time=0.7)
            self.wait(0.2)

            # ── VÒNG 1: Các nỗ lực cốt lõi xung quanh ──
            ring1 = VGroup()
            for a in np.linspace(0, TAU, 5, endpoint=False):
                # Tính tọa độ lệch dựa trên tâm mới dịch chuyển
                pos = center.get_center() + 1.3 * np.array([np.cos(a), np.sin(a), 0])
                d = Dot(pos, radius=0.07, color=ACADEMIA)
                ring1.add(d)

            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in ring1], lag_ratio=0.1), run_time=1.0)

            # Vẽ đường nối từ nhân ra Vòng 1
            lines1 = VGroup(*[
                Line(center.get_center(), d.get_center(), color=ACADEMIA, stroke_width=2).set_opacity(0.5)
                for d in ring1
            ])
            self.play(Create(lines1), run_time=0.6)

            # ── VÒNG 2: Mở rộng ra toàn bộ cộng đồng đại chúng ──
            ring2 = VGroup()
            for a in np.linspace(0, TAU, 12, endpoint=False):
                # Bán kính rộng hơn (2.5) ôm gọn không gian giữa màn hình
                pos = center.get_center() + 2.5 * np.array([np.cos(a), np.sin(a), 0])
                d = Dot(pos, radius=0.05, color=NEUTRAL).set_opacity(0.7)
                ring2.add(d)

            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in ring2], lag_ratio=0.05), run_time=1.2)

            # Sửa lỗi thuật toán liên kết mạng lưới: Nối từ Vòng 1 ra Vòng 2 tạo cấu trúc phân cấp cực đẹp
            lines2 = VGroup()
            for d2 in ring2:
                # Tìm node gần nhất ở vòng 1 để nối dây vào
                closest_d1 = min(ring1, key=lambda d: np.linalg.norm(d.get_center() - d2.get_center()))
                lines2.add(
                    Line(closest_d1.get_center(), d2.get_center(), color=ACADEMIA, stroke_width=1.2).set_opacity(0.25)
                )

            self.play(Create(lines2), run_time=1.2)
            self.wait(0.3)

            # Chữ kết luận đóng đinh sát cạnh đáy, tránh xa vùng thắt nút mạng lưới phía trên
            community = T(
                "ACADEMIC AI COMMUNITY",
                26,
                ACADEMIA,
                weight=BOLD,
            ).to_edge(DOWN, buff=0.6)

            self.play(FadeIn(community, shift=UP * 0.15), run_time=0.8)
            self.wait(1.5)

        clear(self)

        # ==========================================================
        # VO19 (03:04–03:19)
        # Open Science Pipeline
        # ==========================================================

        hdr = T(
            "CHIA SẺ ĐỂ CÙNG TIẾN BỘ",
            24,
            ACADEMIA,
            weight=BOLD,
        ).to_edge(UP)

        infra = mk_rbox(
            "Hạ tầng\nchia sẻ",
            2.8,
            1.1,
            ACADEMIA,
            fs=16,
        ).shift(UP * 2.2)

        data = mk_rbox(
            "Dữ liệu\nchất lượng",
            2.8,
            1.1,
            SUCCESS,
            fs=16,
        )

        research = mk_rbox(
            "Hiểu biết\nkhoa học",
            2.8,
            1.1,
            HIGHLIGHT,
            fs=16,
        ).shift(DOWN * 2.2)

        arrow1 = Arrow(
            infra.get_bottom(),
            data.get_top(),
            buff=0.15,
            stroke_width=4,
        )

        arrow2 = Arrow(
            data.get_bottom(),
            research.get_top(),
            buff=0.15,
            stroke_width=4,
        )

        hub = Circle(
            radius=1.1,
            color=HIGHLIGHT,
            fill_opacity=0.12,
        )

        hub_text = T(
            "OPEN\nSCIENCE",
            22,
            HIGHLIGHT,
            weight=BOLD,
        ).move_to(hub)

        outputs = VGroup(
            T("Papers", 18, ACADEMIA),
            T("Open Models", 18, SUCCESS),
            T("Datasets", 18, WHITE),
            T("Tools", 18, HIGHLIGHT),
        )

        outputs.arrange(RIGHT, buff=0.8)
        outputs.scale(0.9)
        outputs.to_edge(DOWN)

        with self.voiceover(
                """
                Nếu cùng chia sẻ hạ tầng tính toán,
                cùng xây dựng dữ liệu chất lượng,
                và cùng công bố những hiểu biết khoa học nghiêm túc,
    
                thì ngay cả những phòng thí nghiệm nhỏ
                cũng có thể tạo ra những công trình có ảnh hưởng lớn.
                """
        ):
            self.play(FadeIn(hdr), run_time=0.5)

            self.play(FadeIn(infra), run_time=1.2)

            self.play(
                GrowArrow(arrow1),
                FadeIn(data),
                run_time=1.2,
            )

            self.play(
                GrowArrow(arrow2),
                FadeIn(research),
                run_time=1.2,
            )

            pipeline = VGroup(
                infra,
                data,
                research,
                arrow1,
                arrow2,
            )

            self.play(
                pipeline.animate.scale(0.75).move_to(LEFT * 3),
                run_time=1.5,
            )

            self.play(
                Create(hub),
                FadeIn(hub_text),
                run_time=1.2,
            )

            self.play(
                LaggedStart(
                    *[
                        FadeIn(o, shift=UP * 0.2)
                        for o in outputs
                    ],
                    lag_ratio=0.15,
                ),
                run_time=2.5,
            )

            self.wait(1)

        clear(self)

        # ==========================================================
        # VO20 (03:19–03:30)
        # Small Tasks -> Revolution
        # ==========================================================

        random.seed(42)

        task_labels = [
            "experiment",
            "benchmark",
            "dataset",
            "training run",
            "paper draft",
            "evaluation",
        ]

        tasks = VGroup()

        positions = [
            LEFT * 3 + UP * 1.2,
            LEFT * 1.5 + DOWN * 0.5,
            ORIGIN,
            RIGHT * 1.8 + UP * 0.8,
            RIGHT * 3 + DOWN * 0.6,
            UP * 2,
        ]

        for txt, pos in zip(task_labels, positions):
            tasks.add(
                T(
                    txt,
                    14,
                    NEUTRAL,
                ).move_to(pos)
            )

        with self.voiceover(
            """
            Bởi vì đôi khi,
            tất cả những gì khoa học cần
            để tạo nên một cuộc cách mạng...
            chỉ là một chuỗi những tác vụ nhỏ lẻ,
            âm thầm chạy trong đêm muộn mà thôi.
            """
        ):
            self.play(
                LaggedStart(
                    *[FadeIn(t) for t in tasks],
                    lag_ratio=0.15
                ),
                run_time=2
            )

            dots = VGroup()

            for t in tasks:
                dots.add(
                    Dot(
                        t.get_center(),
                        radius=0.05,
                        color=ACADEMIA
                    )
                )

            self.play(
                ReplacementTransform(
                    tasks,
                    dots
                ),
                run_time=1.2
            )

            links = VGroup()

            for i in range(len(dots)):
                for j in range(i + 1, len(dots)):
                    if np.linalg.norm(
                        dots[i].get_center()
                        - dots[j].get_center()
                    ) < 3:
                        links.add(
                            Line(
                                dots[i].get_center(),
                                dots[j].get_center(),
                                color=ACADEMIA,
                                stroke_opacity=0.3,
                            )
                        )

            self.play(
                Create(links),
                run_time=1.2
            )

            quote = VGroup(
                T(
                    "KHOA HỌC KHÔNG TIẾN LÊN",
                    24,
                    WHITE,
                    weight=BOLD,
                ),
                T(
                    "NHỜ MỘT KHOẢNH KHẮC THIÊN TÀI",
                    24,
                    HIGHLIGHT,
                    weight=BOLD,
                ),
                T(
                    "MÀ NHỜ HÀNG NGHÌN NỖ LỰC NHỎ ĐƯỢC KẾT NỐI",
                    22,
                    ACADEMIA,
                    weight=BOLD,
                ),
            ).arrange(DOWN, buff=0.25)

            quote.move_to(DOWN * 2)

            self.play(
                FadeIn(
                    quote,
                    shift=UP * 0.2
                ),
                run_time=2.5
            )

            self.wait(1)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=2
        )

# ══════════════════════════════════════════════════════════════════════════════
# P5_Complete — Unified scene combining all 5 scenes with chapter transitions
# ══════════════════════════════════════════════════════════════════════════════
class P5_Complete(VoiceoverScene):
    def construct(self):
        self.set_speech_service(svc())
        self.set_speech_service = lambda *a, **kw: None   # lock re-init

        P5_RLReasoning.construct(self)
        P5_Summary.construct(self)
        P5_BoldIdeas.construct(self)
        P5_Collaboration.construct(self)
        P5_CallToAction.construct(self)
