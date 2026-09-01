# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
fig.patch.set_facecolor('#0F172A')
ax.set_facecolor('#0F172A')

def draw_card(ax, x, y, w, h, title, lines, header_color, border_color):
    rect = patches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.03",
        facecolor="#1E293B", edgecolor=border_color, linewidth=2, zorder=3
    )
    ax.add_patch(rect)
    
    h_bar = 0.04
    header = patches.FancyBboxPatch(
        (x - w/2, y + h/2 - h_bar), w, h_bar,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=header_color, edgecolor=header_color, linewidth=1, zorder=4
    )
    ax.add_patch(header)
    
    ax.text(x, y + h/2 - h_bar/2, title, ha='center', va='center', color='#FFFFFF', fontsize=10, fontweight='bold', zorder=5)
    
    content_y = y + h/2 - h_bar - 0.025
    for line in lines:
        ax.text(x - w/2 + 0.02, content_y, line, ha='left', va='top', color='#E2E8F0', fontsize=8.5, zorder=5)
        content_y -= 0.03

cx, cy = 0.5, 0.5
core = patches.FancyBboxPatch(
    (cx - 0.16, cy - 0.05), 0.32, 0.10,
    boxstyle="round,pad=0.02,rounding_size=0.04",
    facecolor="#2563EB", edgecolor="#60A5FA", linewidth=3, zorder=6
)
ax.add_patch(core)
ax.text(cx, cy + 0.015, "ESTRATEGIA DE TESTES", ha='center', va='center', color='#FFFFFF', fontsize=12, fontweight='bold', zorder=7)
ax.text(cx, cy - 0.02, "EBAC-SHOP (QE MASTER PLAN)", ha='center', va='center', color='#93C5FD', fontsize=9.5, fontweight='bold', zorder=7)

cards = [
    {
        "x": 0.22, "y": 0.82, "w": 0.36, "h": 0.22,
        "title": "1. GOVERNANCA & OBJETIVOS",
        "header_color": "#0284C7", "border_color": "#38BDF8",
        "lines": [
            "- Missao: Confiabilidade, Resiliencia e Automacao",
            "- Papeis: QE (Estrategia/CI), Devs (Unit), PO (DoR/DoD)",
            "- Cultura: Shift-Left Testing & Engenharia de Qualidade",
            "- Abordagem: BDD (Gherkin) com foco no comportamento"
        ]
    },
    {
        "x": 0.78, "y": 0.82, "w": 0.36, "h": 0.22,
        "title": "2. NIVEIS & PIRAMIDE DE TESTE",
        "header_color": "#4F46E5", "border_color": "#818CF8",
        "lines": [
            "- Unidade: Logica de negocio e calculos de desconto",
            "- API Rest: Contratos JSON e regras de cupons (Supertest)",
            "- E2E Web: Fluxos criticos de compra e login (Cypress)",
            "- Mobile: Catalogo e vitrine de produtos (WebdriverIO)",
            "- Performance: Carga com 20 VUs e SLAs rigidos (K6)"
        ]
    },
    {
        "x": 0.22, "y": 0.50, "w": 0.36, "h": 0.22,
        "title": "3. TECNICAS FORMAIS DE TESTE",
        "header_color": "#D97706", "border_color": "#FBBF24",
        "lines": [
            "- Particao de Equivalencia (EP): Classes validas/invalidas",
            "- Analise do Valor Limite (BVA): Limites 10 itens / R$ 990",
            "- Tabela de Decisao: Matriz de desconto (10% e 15%)",
            "- Transicao de Estados: Bloqueio 15 min apos 3 falhas"
        ]
    },
    {
        "x": 0.78, "y": 0.50, "w": 0.36, "h": 0.22,
        "title": "4. STACK & TESTING PATTERNS",
        "header_color": "#059669", "border_color": "#34D399",
        "lines": [
            "- UI: Cypress com Page Object Model (POM)",
            "- API: Supertest + Jest + Ajv (JSON Schema)",
            "- Mobile: WebdriverIO + Appium + UiAutomator2",
            "- Performance: K6 (20 VUs, 2min duracao, 20s ramp-up)",
            "- Relatorios: Mochawesome HTML Reports com prints"
        ]
    },
    {
        "x": 0.22, "y": 0.18, "w": 0.36, "h": 0.22,
        "title": "5. AMBIENTES & INFRAESTRUTURA",
        "header_color": "#DB2777", "border_color": "#F472B6",
        "lines": [
            "- Producao / Staging: lojaebac.ebaconline.art.br",
            "- Docker Hub Local: ernestosbarbosa/lojaebac (Porta 80)",
            "- Banco de Dados: ernestosbarbosa/lojaebacdb (Porta 3306)",
            "- Rede: ebac-network (Bridge attachable)"
        ]
    },
    {
        "x": 0.78, "y": 0.18, "w": 0.36, "h": 0.22,
        "title": "6. CI/CD & REPOSITORIO GITHUB",
        "header_color": "#7C3AED", "border_color": "#A78BFA",
        "lines": [
            "- Repositorio: TCC-EBAC-QE (Publico)",
            "- GitHub Actions: Workflows test-ui, test-api e test-k6",
            "- Triggers: Push na branch main e Pull Requests",
            "- Artefatos: Upload automatico de relatorios e evidencias"
        ]
    }
]

for card in cards:
    ax.annotate(
        "", xy=(card["x"], card["y"]), xytext=(cx, cy),
        arrowprops=dict(arrowstyle="-", color=card["border_color"], lw=2.5, linestyle="--", shrinkA=45, shrinkB=60)
    )
    draw_card(ax, card["x"], card["y"], card["w"], card["h"], card["title"], card["lines"], card["header_color"], card["border_color"])

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

out_path = r"C:\Users\leona\TCC-EBAC-QE\docs\mapa-mental-estrategia.png"
plt.tight_layout()
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Mapa mental gerado com sucesso!")
