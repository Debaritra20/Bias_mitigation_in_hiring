import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64
from fpdf import FPDF
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Bias Detection Dashboard | HR Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme CSS Styling
st.markdown("""
    <style>
        :root {
            --primary: #4a8fe7;
            --secondary: #30c971;
            --danger: #ff6b6b;
            --dark: #121212;
            --light: #f8f9fa;
            --accent: #9b59b6;
            --warning: #ffbe0b;
            --card-bg: #1e1e1e;
            --sidebar-bg: #1a1a1a;
        }
        
        body {
            color: var(--light);
        }
        
        .main { 
            background-color: var(--dark);
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--light);
        }
        
        .stApp {
            background-color: var(--dark);
        }
        
        .header {
            color: var(--light);
            border-bottom: 2px solid var(--primary);
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }
        
        .metric-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            border-left: 4px solid var(--primary);
            height: 100%;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            color: var(--light);
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--light);
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #b0b0b0;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }
        
        .feature-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
            border: 1px solid #333;
            color: var(--light);
        }
        
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 10px !important;
            border: 1px solid #444 !important;
            background-color: var(--card-bg) !important;
            color: var(--light) !important;
        }
        
        .stTextInput input {
            background-color: var(--card-bg) !important;
            color: var(--light) !important;
            border: 1px solid #444 !important;
        }
        
        .stButton>button {
            border-radius: 10px !important;
            background-color: var(--primary) !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(74, 143, 231, 0.5) !important;
        }
        
        .stDownloadButton>button {
            border-radius: 10px !important;
            background-color: var(--secondary) !important;
            color: white !important;
            border: none !important;
        }
        
        .st-expander {
            border-radius: 10px !important;
            border: 1px solid #444 !important;
            background-color: var(--card-bg) !important;
        }
        
        .stAlert {
            border-radius: 10px !important;
            background-color: var(--card-bg) !important;
        }
        
        .info-banner {
            background: linear-gradient(135deg, #2a3a4a 0%, #1a2a3a 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border-left: 5px solid var(--primary);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            color: var(--light);
        }
        
        .info-banner h3 {
            color: var(--light);
            margin-top: 0;
        }
        
        .tab-content {
            padding: 1.5rem 0;
        }
        
        /* Tooltip styling */
        .stTooltip {
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            background-color: var(--card-bg) !important;
            color: var(--light) !important;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
            background-color: var(--card-bg) !important;
            color: var(--light) !important;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: var(--sidebar-bg) !important;
        }
        
        /* Plotly chart background */
        .js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg {
            background-color: transparent !important;
        }
        
        /* Matplotlib dark theme */
        .dark-background {
            background-color: #1e1e1e !important;
        }
        
        /* Change text color throughout the app */
        h1, h2, h3, h4, h5, h6, p, div, span {
            color: var(--light) !important;
        }
        
        /* Change dataframe text color */
        .dataframe th, .dataframe td {
            color: var(--light) !important;
        }
        
        /* Change select box text color */
        .st-b7, .st-b8, .st-b9, .st-ba, .st-bb, .st-bc, .st-bd, .st-be, .st-bf, .st-bg, .st-bh, .st-bi, .st-bj, .st-bk, .st-bl, .st-bm, .st-bn, .st-bo, .st-bp, .st-bq, .st-br, .st-bs, .st-bt, .st-bu, .st-bv, .st-bw, .st-bx, .st-by, .st-bz, .st-c0, .st-c1, .st-c2, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7, .st-c8, .st-c9, .st-ca, .st-cb, .st-cc, .st-cd, .st-ce, .st-cf, .st-cg, .st-ch, .st-ci, .st-cj, .st-ck, .st-cl, .st-cm, .st-cn, .st-co, .st-cp, .st-cq, .st-cr, .st-cs, .st-ct, .st-cu, .st-cv, .st-cw, .st-cx, .st-cy, .st-cz, .st-d0, .st-d1, .st-d2, .st-d3, .st-d4, .st-d5, .st-d6, .st-d7, .st-d8, .st-d9, .st-da, .st-db, .st-dc, .st-dd, .st-de, .st-df, .st-dg, .st-dh, .st-di, .st-dj, .st-dk, .st-dl, .st-dm, .st-dn, .st-do, .st-dp, .st-dq, .st-dr, .st-ds, .st-dt, .st-du, .st-dv, .st-dw, .st-dx, .st-dy, .st-dz, .st-e0, .st-e1, .st-e2, .st-e3, .st-e4, .st-e5, .st-e6, .st-e7, .st-e8, .st-e9, .st-ea, .st-eb, .st-ec, .st-ed, .st-ee, .st-ef, .st-eg, .st-eh, .st-ei, .st-ej, .st-ek, .st-el, .st-em, .st-en, .st-eo, .st-ep, .st-eq, .st-er, .st-es, .st-et, .st-eu, .st-ev, .st-ew, .st-ex, .st-ey, .st-ez, .st-f0, .st-f1, .st-f2, .st-f3, .st-f4, .st-f5, .st-f6, .st-f7, .st-f8, .st-f9, .st-fa, .st-fb, .st-fc, .st-fd, .st-fe, .st-ff, .st-fg, .st-fh, .st-fi, .st-fj, .st-fk, .st-fl, .st-fm, .st-fn, .st-fo, .st-fp, .st-fq, .st-fr, .st-fs, .st-ft, .st-fu, .st-fv, .st-fw, .st-fx, .st-fy, .st-fz, .st-g0, .st-g1, .st-g2, .st-g3, .st-g4, .st-g5, .st-g6, .st-g7, .st-g8, .st-g9, .st-ga, .st-gb, .st-gc, .st-gd, .st-ge, .st-gf, .st-gg, .st-gh, .st-gi, .st-gj, .st-gk, .st-gl, .st-gm, .st-gn, .st-go, .st-gp, .st-gq, .st-gr, .st-gs, .st-gt, .st-gu, .st-gv, .st-gw, .st-gx, .st-gy, .st-gz, .st-h0, .st-h1, .st-h2, .st-h3, .st-h4, .st-h5, .st-h6, .st-h7, .st-h8, .st-h9, .st-ha, .st-hb, .st-hc, .st-hd, .st-he, .st-hf, .st-hg, .st-hh, .st-hi, .st-hj, .st-hk, .st-hl, .st-hm, .st-hn, .st-ho, .st-hp, .st-hq, .st-hr, .st-hs, .st-ht, .st-hu, .st-hv, .st-hw, .st-hx, .st-hy, .st-hz, .st-i0, .st-i1, .st-i2, .st-i3, .st-i4, .st-i5, .st-i6, .st-i7, .st-i8, .st-i9, .st-ia, .st-ib, .st-ic, .st-id, .st-ie, .st-if, .st-ig, .st-ih, .st-ii, .st-ij, .st-ik, .st-il, .st-im, .st-in, .st-io, .st-ip, .st-iq, .st-ir, .st-is, .st-it, .st-iu, .st-iv, .st-iw, .st-ix, .st-iy, .st-iz, .st-j0, .st-j1, .st-j2, .st-j3, .st-j4, .st-j5, .st-j6, .st-j7, .st-j8, .st-j9, .st-ja, .st-jb, .st-jc, .st-jd, .st-je, .st-jf, .st-jg, .st-jh, .st-ji, .st-jj, .st-jk, .st-jl, .st-jm, .st-jn, .st-jo, .st-jp, .st-jq, .st-jr, .st-js, .st-jt, .st-ju, .st-jv, .st-jw, .st-jx, .st-jy, .st-jz, .st-k0, .st-k1, .st-k2, .st-k3, .st-k4, .st-k5, .st-k6, .st-k7, .st-k8, .st-k9, .st-ka, .st-kb, .st-kc, .st-kd, .st-ke, .st-kf, .st-kg, .st-kh, .st-ki, .st-kj, .st-kk, .st-kl, .st-km, .st-kn, .st-ko, .st-kp, .st-kq, .st-kr, .st-ks, .st-kt, .st-ku, .st-kv, .st-kw, .st-kx, .st-ky, .st-kz, .st-l0, .st-l1, .st-l2, .st-l3, .st-l4, .st-l5, .st-l6, .st-l7, .st-l8, .st-l9, .st-la, .st-lb, .st-lc, .st-ld, .st-le, .st-lf, .st-lg, .st-lh, .st-li, .st-lj, .st-lk, .st-ll, .st-lm, .st-ln, .st-lo, .st-lp, .st-lq, .st-lr, .st-ls, .st-lt, .st-lu, .st-lv, .st-lw, .st-lx, .st-ly, .st-lz, .st-m0, .st-m1, .st-m2, .st-m3, .st-m4, .st-m5, .st-m6, .st-m7, .st-m8, .st-m9, .st-ma, .st-mb, .st-mc, .st-md, .st-me, .st-mf, .st-mg, .st-mh, .st-mi, .st-mj, .st-mk, .st-ml, .st-mm, .st-mn, .st-mo, .st-mp, .st-mq, .st-mr, .st-ms, .st-mt, .st-mu, .st-mv, .st-mw, .st-mx, .st-my, .st-mz, .st-n0, .st-n1, .st-n2, .st-n3, .st-n4, .st-n5, .st-n6, .st-n7, .st-n8, .st-n9, .st-na, .st-nb, .st-nc, .st-nd, .st-ne, .st-nf, .st-ng, .st-nh, .st-ni, .st-nj, .st-nk, .st-nl, .st-nm, .st-nn, .st-no, .st-np, .st-nq, .st-nr, .st-ns, .st-nt, .st-nu, .st-nv, .st-nw, .st-nx, .st-ny, .st-nz, .st-o0, .st-o1, .st-o2, .st-o3, .st-o4, .st-o5, .st-o6, .st-o7, .st-o8, .st-o9, .st-oa, .st-ob, .st-oc, .st-od, .st-oe, .st-of, .st-og, .st-oh, .st-oi, .st-oj, .st-ok, .st-ol, .st-om, .st-on, .st-oo, .st-op, .st-oq, .st-or, .st-os, .st-ot, .st-ou, .st-ov, .st-ow, .st-ox, .st-oy, .st-oz, .st-p0, .st-p1, .st-p2, .st-p3, .st-p4, .st-p5, .st-p6, .st-p7, .st-p8, .st-p9, .st-pa, .st-pb, .st-pc, .st-pd, .st-pe, .st-pf, .st-pg, .st-ph, .st-pi, .st-pj, .st-pk, .st-pl, .st-pm, .st-pn, .st-po, .st-pp, .st-pq, .st-pr, .st-ps, .st-pt, .st-pu, .st-pv, .st-pw, .st-px, .st-py, .st-pz, .st-q0, .st-q1, .st-q2, .st-q3, .st-q4, .st-q5, .st-q6, .st-q7, .st-q8, .st-q9, .st-qa, .st-qb, .st-qc, .st-qd, .st-qe, .st-qf, .st-qg, .st-qh, .st-qi, .st-qj, .st-qk, .st-ql, .st-qm, .st-qn, .st-qo, .st-qp, .st-qq, .st-qr, .st-qs, .st-qt, .st-qu, .st-qv, .st-qw, .st-qx, .st-qy, .st-qz, .st-r0, .st-r1, .st-r2, .st-r3, .st-r4, .st-r5, .st-r6, .st-r7, .st-r8, .st-r9, .st-ra, .st-rb, .st-rc, .st-rd, .st-re, .st-rf, .st-rg, .st-rh, .st-ri, .st-rj, .st-rk, .st-rl, .st-rm, .st-rn, .st-ro, .st-rp, .st-rq, .st-rr, .st-rs, .st-rt, .st-ru, .st-rv, .st-rw, .st-rx, .st-ry, .st-rz, .st-s0, .st-s1, .st-s2, .st-s3, .st-s4, .st-s5, .st-s6, .st-s7, .st-s8, .st-s9, .st-sa, .st-sb, .st-sc, .st-sd, .st-se, .st-sf, .st-sg, .st-sh, .st-si, .st-sj, .st-sk, .st-sl, .st-sm, .st-sn, .st-so, .st-sp, .st-sq, .st-sr, .st-ss, .st-st, .st-su, .st-sv, .st-sw, .st-sx, .st-sy, .st-sz, .st-t0, .st-t1, .st-t2, .st-t3, .st-t4, .st-t5, .st-t6, .st-t7, .st-t8, .st-t9, .st-ta, .st-tb, .st-tc, .st-td, .st-te, .st-tf, .st-tg, .st-th, .st-ti, .st-tj, .st-tk, .st-tl, .st-tm, .st-tn, .st-to, .st-tp, .st-tq, .st-tr, .st-ts, .st-tt, .st-tu, .st-tv, .st-tw, .st-tx, .st-ty, .st-tz, .st-u0, .st-u1, .st-u2, .st-u3, .st-u4, .st-u5, .st-u6, .st-u7, .st-u8, .st-u9, .st-ua, .st-ub, .st-uc, .st-ud, .st-ue, .st-uf, .st-ug, .st-uh, .st-ui, .st-uj, .st-uk, .st-ul, .st-um, .st-un, .st-uo, .st-up, .st-uq, .st-ur, .st-us, .st-ut, .st-uu, .st-uv, .st-uw, .st-ux, .st-uy, .st-uz, .st-v0, .st-v1, .st-v2, .st-v3, .st-v4, .st-v5, .st-v6, .st-v7, .st-v8, .st-v9, .st-va, .st-vb, .st-vc, .st-vd, .st-ve, .st-vf, .st-vg, .st-vh, .st-vi, .st-vj, .st-vk, .st-vl, .st-vm, .st-vn, .st-vo, .st-vp, .st-vq, .st-vr, .st-vs, .st-vt, .st-vu, .st-vv, .st-vw, .st-vx, .st-vy, .st-vz, .st-w0, .st-w1, .st-w2, .st-w3, .st-w4, .st-w5, .st-w6, .st-w7, .st-w8, .st-w9, .st-wa, .st-wb, .st-wc, .st-wd, .st-we, .st-wf, .st-wg, .st-wh, .st-wi, .st-wj, .st-wk, .st-wl, .st-wm, .st-wn, .st-wo, .st-wp, .st-wq, .st-wr, .st-ws, .st-wt, .st-wu, .st-wv, .st-ww, .st-wx, .st-wy, .st-wz, .st-x0, .st-x1, .st-x2, .st-x3, .st-x4, .st-x5, .st-x6, .st-x7, .st-x8, .st-x9, .st-xa, .st-xb, .st-xc, .st-xd, .st-xe, .st-xf, .st-xg, .st-xh, .st-xi, .st-xj, .st-xk, .st-xl, .st-xm, .st-xn, .st-xo, .st-xp, .st-xq, .st-xr, .st-xs, .st-xt, .st-xu, .st-xv, .st-xw, .st-xx, .st-xy, .st-xz, .st-y0, .st-y1, .st-y2, .st-y3, .st-y4, .st-y5, .st-y6, .st-y7, .st-y8, .st-y9, .st-ya, .st-yb, .st-yc, .st-yd, .st-ye, .st-yf, .st-yg, .st-yh, .st-yi, .st-yj, .st-yk, .st-yl, .st-ym, .st-yn, .st-yo, .st-yp, .st-yq, .st-yr, .st-ys, .st-yt, .st-yu, .st-yv, .st-yw, .st-yx, .st-yy, .st-yz, .st-z0, .st-z1, .st-z2, .st-z3, .st-z4, .st-z5, .st-z6, .st-z7, .st-z8, .st-z9, .st-za, .st-zb, .st-zc, .st-zd, .st-ze, .st-zf, .st-zg, .st-zh, .st-zi, .st-zj, .st-zk, .st-zl, .st-zm, .st-zn, .st-zo, .st-zp, .st-zq, .st-zr, .st-zs, .st-zt, .st-zu, .st-zv, .st-zw, .st-zx, .st-zy, .st-zz, .st-10, .st-11, .st-12, .st-13, .st-14, .st-15, .st-16, .st-17, .st-18, .st-19, .st-1a, .st-1b, .st-1c, .st-1d, .st-1e, .st-1f, .st-1g, .st-1h, .st-1i, .st-1j, .st-1k, .st-1l, .st-1m, .st-1n, .st-1o, .st-1p, .st-1q, .st-1r, .st-1s, .st-1t, .st-1u, .st-1v, .st-1w, .st-1x, .st-1y, .st-1z {
            color: var(--light) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=HR+Analytics", width=200)
    st.markdown("## Data Configuration")
    
    uploaded_file = st.file_uploader(
        "📁 Upload Hiring Dataset", 
        type=["csv", "xlsx"],
        help="Upload your CSV or Excel file containing hiring data for analysis"
    )
    
    st.markdown("---")
    st.markdown("### Analysis Parameters")
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        target_col = st.selectbox(
            "🎯 Target Variable",
            options=df.columns,
            index=len(df.columns)-1 if 'employed_yes' in df.columns else 0,
            help="Select the variable representing the hiring outcome"
        )
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        feature_col = st.selectbox(
            "📊 Feature to Analyze",
            options=numeric_cols,
            help="Select a numeric feature to analyze against the target variable"
        )
        
        st.markdown("---")
        st.markdown("### Export Results")
        
        # Create a session state to store figures for PDF export
        if 'figures' not in st.session_state:
            st.session_state.figures = []
        
        # Function to generate PDF report
        def generate_pdf_report():
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Add title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Bias Detection Analysis Report", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
            pdf.ln(10)
            
            # Add dataset overview
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt="1. Dataset Overview", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Total Records: {len(df)}", ln=True)
            pdf.cell(200, 10, txt=f"Features: {len(df.columns)}", ln=True)
            if target_col in df.columns:
                target_counts = df[target_col].value_counts()
                pdf.cell(200, 10, txt=f"Positive Outcomes: {target_counts.get(1, 0)}", ln=True)
                employment_rate = df[target_col].mean() * 100
                pdf.cell(200, 10, txt=f"Success Rate: {employment_rate:.1f}%", ln=True)
            pdf.ln(10)
            
            # Add correlation matrix
            if 'corr_matrix' in st.session_state.figures:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="2. Correlation Analysis", ln=True)
                pdf.image(st.session_state.figures['corr_matrix'], x=10, w=180)
                pdf.ln(5)
                
                # Add correlation interpretation
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, txt="Interpretation Guide:\n" +
                    "- Values close to +1 indicate strong positive correlation\n" +
                    "- Values close to -1 indicate strong negative correlation\n" +
                    "- Values near 0 suggest no linear relationship\n\n" +
                    "Look for unexpected correlations between protected attributes (gender, race) and outcomes.")
                pdf.ln(10)
            
            # Add feature analysis
            if 'feature_analysis' in st.session_state.figures:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt=f"3. Feature Analysis: {feature_col}", ln=True)
                pdf.image(st.session_state.figures['feature_analysis'], x=10, w=180)
                pdf.ln(10)
            
            # Add protected attribute analysis
            if 'protected_analysis' in st.session_state.figures:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, txt="4. Protected Attribute Analysis", ln=True)
                pdf.image(st.session_state.figures['protected_analysis'], x=10, w=180)
                pdf.ln(10)
            
            # Save the PDF to a buffer
            pdf_buffer = BytesIO()
            pdf.output(pdf_buffer)
            pdf_buffer.seek(0)
            return pdf_buffer
        
        # Button to generate and download PDF
        if st.button("📄 Generate Full PDF Report"):
            with st.spinner("Generating PDF report..."):
                # Save figures to session state
                st.session_state.figures = {}
                
                # Save correlation matrix
                corr = df.corr(numeric_only=True)
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, ax=ax)
                buf = BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                buf.seek(0)
                st.session_state.figures['corr_matrix'] = buf
                
                # Save feature analysis
                if feature_col in df.columns:
                    fig = px.histogram(df, x=feature_col, color_discrete_sequence=['#3498db'], nbins=30)
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    feature_buf = BytesIO()
                    fig.write_image(feature_buf, format="png", width=800, height=500)
                    feature_buf.seek(0)
                    st.session_state.figures['feature_analysis'] = feature_buf
                
                # Save protected attribute analysis if available
                protected_attributes = [col for col in df.columns if col.lower() in ['gender', 'sex', 'race', 'age', 'ethnicity']]
                if protected_attributes and target_col in df.columns:
                    selected_protected = protected_attributes[0]
                    success_rates = df.groupby(selected_protected)[target_col].mean() * 100
                    fig = px.bar(
                        x=success_rates.index,
                        y=success_rates.values,
                        color=success_rates.index.astype(str),
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        labels={'x': selected_protected, 'y': 'Success Rate (%)'},
                        text=success_rates.round(1).astype(str) + '%'
                    )
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    protected_buf = BytesIO()
                    fig.write_image(protected_buf, format="png", width=800, height=500)
                    protected_buf.seek(0)
                    st.session_state.figures['protected_analysis'] = protected_buf
                
                # Generate and download PDF
                pdf_buffer = generate_pdf_report()
                st.success("PDF report generated successfully!")
                st.download_button(
                    label="⬇️ Download Full Report",
                    data=pdf_buffer,
                    file_name=f"bias_detection_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

# Main Content
st.title("🔍 Bias Detection in Hiring Data")
st.markdown("""
    <div class='info-banner'>
        <h3>Comprehensive Hiring Bias Analysis</h3>
        <p>This advanced dashboard helps identify potential biases in hiring data by analyzing relationships between candidate attributes and employment outcomes. 
        Explore correlations, visualize distributions, and detect disparities across protected groups.</p>
    </div>
""", unsafe_allow_html=True)

if uploaded_file is not None:
    # Data Overview Section
    st.markdown("## 📋 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{:,}</div>
                <div class="metric-label">Total Records</div>
            </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Features</div>
            </div>
        """.format(len(df.columns)), unsafe_allow_html=True)
    
    with col3:
        if target_col in df.columns:
            target_counts = df[target_col].value_counts()
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{:,}</div>
                    <div class="metric-label">Positive Outcomes</div>
                </div>
            """.format(target_counts.get(1, 0)), unsafe_allow_html=True)
    
    with col4:
        if target_col in df.columns:
            employment_rate = df[target_col].mean() * 100
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{:.1f}%</div>
                    <div class="metric-label">Success Rate</div>
                </div>
            """.format(employment_rate), unsafe_allow_html=True)
    
    # Data Preview Section
    with st.expander("🔎 View Raw Data & Statistics", expanded=False):
        tab1, tab2 = st.tabs(["📄 Raw Data", "📈 Statistics"])
        
        with tab1:
            st.dataframe(df.style.background_gradient(cmap='Blues'), height=300)
        
        with tab2:
            st.markdown("### Descriptive Statistics")
            st.dataframe(df.describe().T.style.background_gradient(cmap='YlOrBr'))
    
    st.markdown("---")
    
    # Correlation Analysis Section
    st.markdown("## 🔗 Correlation Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Set dark background for matplotlib
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 8))
        
        corr = df.corr(numeric_only=True)
        sns.heatmap(
            corr, 
            cmap="coolwarm", 
            annot=True, 
            fmt=".2f", 
            linewidths=0.5, 
            ax=ax,
            center=0,
            annot_kws={"size": 10}
        )
        ax.set_title("Feature Correlation Matrix", fontsize=14, pad=20)
        st.pyplot(fig)
        
        # Save correlation matrix for PDF
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        st.session_state.corr_matrix = buf
    
    with col2:
        st.markdown("### Interpretation Guide")
        st.markdown("""
            <div style='background-color: #2a2a2a; padding: 1rem; border-radius: 10px;'>
                <p><strong>Correlation Values:</strong></p>
                <ul style='margin-top: 0; padding-left: 1.2rem;'>
                    <li><strong>+0.7 to +1.0:</strong> Strong positive relationship</li>
                    <li><strong>+0.3 to +0.7:</strong> Moderate positive relationship</li>
                    <li><strong>-0.3 to +0.3:</strong> Weak or no relationship</li>
                    <li><strong>-0.7 to -0.3:</strong> Moderate negative relationship</li>
                    <li><strong>-1.0 to -0.7:</strong> Strong negative relationship</li>
                </ul>
                <p><strong>Warning:</strong> Correlation ≠ Causation. Investigate unexpected relationships.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature Analysis Section
    st.markdown("## 📊 Feature Analysis")
    
    if feature_col in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### Distribution of {feature_col}")
            
            if df[feature_col].nunique() > 10:
                # Continuous variable - histogram
                fig = px.histogram(
                    df, 
                    x=feature_col,
                    color_discrete_sequence=['#4a8fe7'],
                    nbins=30,
                    marginal="box",
                    title=f"Distribution of {feature_col}"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    hovermode="x unified",
                    font=dict(color='white'),
                    title_font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Categorical variable - bar chart
                value_counts = df[feature_col].value_counts().sort_index()
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    color=value_counts.index.astype(str),
                    color_discrete_sequence=px.colors.qualitative.Dark24,
                    labels={'x': feature_col, 'y': 'Count'},
                    title=f"Distribution of {feature_col}"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    showlegend=False,
                    hovermode="x unified",
                    font=dict(color='white'),
                    title_font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if target_col in df.columns:
                st.markdown(f"### {feature_col} vs {target_col}")
                
                if df[target_col].nunique() == 2:
                    # Binary target - boxplot or bar chart
                    if df[feature_col].nunique() > 10:
                        fig = px.box(
                            df,
                            x=target_col,
                            y=feature_col,
                            color=target_col,
                            color_discrete_sequence=['#ff6b6b', '#30c971'],
                            points="all",
                            title=f"{feature_col} by {target_col}"
                        )
                    else:
                        cross_tab = pd.crosstab(df[feature_col], df[target_col], normalize='index') * 100
                        fig = px.bar(
                            cross_tab,
                            barmode='group',
                            color_discrete_sequence=['#ff6b6b', '#30c971'],
                            labels={'value': 'Percentage', 'variable': target_col},
                            title=f"Success Rate by {feature_col}"
                        )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        hovermode="x unified",
                        font=dict(color='white'),
                        title_font=dict(color='white')
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # Protected Attribute Analysis
    st.markdown("---")
    st.markdown("## 🛡 Protected Attribute Analysis")
    
    protected_attributes = [col for col in df.columns if col.lower() in ['gender', 'sex', 'race', 'age', 'ethnicity']]
    
    if protected_attributes:
        selected_protected = st.selectbox(
            "Select protected attribute to analyze",
            options=protected_attributes,
            key="protected_attr"
        )
        
        if selected_protected in df.columns and target_col in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {selected_protected} Distribution")
                value_counts = df[selected_protected].value_counts(normalize=True) * 100
                fig = px.pie(
                    names=value_counts.index,
                    values=value_counts.values,
                    color_discrete_sequence=px.colors.qualitative.Dark24,
                    hole=0.4,
                    title=f"Distribution of {selected_protected}"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    showlegend=True,
                    font=dict(color='white'),
                    title_font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"### Success Rate by {selected_protected}")
                success_rates = df.groupby(selected_protected)[target_col].mean() * 100
                fig = px.bar(
                    x=success_rates.index,
                    y=success_rates.values,
                    color=success_rates.index.astype(str),
                    color_discrete_sequence=px.colors.qualitative.Dark24,
                    labels={'x': selected_protected, 'y': 'Success Rate (%)'},
                    text=success_rates.round(1).astype(str) + '%',
                    title=f"Success Rate by {selected_protected}"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    showlegend=False,
                    yaxis_range=[0, 100],
                    font=dict(color='white'),
                    title_font=dict(color='white')
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate disparity
                max_rate = success_rates.max()
                min_rate = success_rates.min()
                disparity = (max_rate - min_rate) / max_rate * 100
                
                if disparity > 20:  # Threshold for warning
                    st.warning(f"⚠️ Significant disparity detected: {disparity:.1f}% difference between highest and lowest success rates")
    else:
        st.warning("No standard protected attributes (gender, race, age) found in the dataset.")

else:
    st.info("👈 Please upload a CSV or Excel file to begin analysis.")
    st.markdown("""
        <div style='background-color: #2a2a2a; padding: 1.5rem; border-radius: 12px;'>
            <h3>Expected Data Structure</h3>
            <p>For optimal analysis, your dataset should include:</p>
            <ul>
                <li><strong>Candidate attributes:</strong> Education, experience, skills, test scores</li>
                <li><strong>Demographic information:</strong> Gender, race, age, ethnicity (if available)</li>
                <li><strong>Outcome variable:</strong> Hiring decision, promotion status, performance rating</li>
            </ul>
            <p>Example columns: <code>sex_male</code>, <code>race_white</code>, <code>years_experience</code>, <code>employed_yes</code></p>
        </div>
    """, unsafe_allow_html=True)