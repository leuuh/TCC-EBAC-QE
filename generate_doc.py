# -*- coding: utf-8 -*-
import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def add_page_number(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_tcc_document():
    doc = docx.Document()
    
    # ----------------------------------------------------
    # CONFIGURAÇÃO DE ESTILO GERAL E MARGENS ABNT
    # ----------------------------------------------------
    # Margens ABNT: Superior 3.0cm (1.18 in), Esquerda 3.0cm (1.18 in), Inferior 2.0cm (0.79 in), Direita 2.0cm (0.79 in)
    section_pre = doc.sections[0]
    section_pre.top_margin = Inches(1.18)
    section_pre.bottom_margin = Inches(0.79)
    section_pre.left_margin = Inches(1.18)
    section_pre.right_margin = Inches(0.79)
    section_pre.header.is_linked_to_previous = False
    
    # Estilo Normal Padrão
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    
    # Funções Auxiliares de Formatação
    def add_p(text, bold_prefix=None, space_after=6, line_spacing=1.5, first_line_indent=0.49, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.alignment = align
        if first_line_indent > 0:
            p.paragraph_format.first_line_indent = Inches(first_line_indent)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = 'Arial'
            rb.font.size = Pt(12)
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        return p

    def add_sec_title(text, num=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(f"{num} {text}".upper())
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        return p

    def add_subsec_title(text, num=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(f"{num} {text}")
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        return p

    def add_subsubsec_title(text, num=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(f"{num} {text}")
        r.bold = True
        r.italic = True
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        set_cell_margins(c, top=140, bottom=140, left=200, right=140)
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:color="CBD5E1"/><w:left w:val="single" w:sz="18" w:color="1E3A8A"/><w:bottom w:val="single" w:sz="4" w:color="CBD5E1"/><w:right w:val="single" w:sz="4" w:color="CBD5E1"/></w:tcBorders>'.format(nsdecls('w'))))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(6)
        p_after.paragraph_format.line_spacing = 1.0

    # ====================================================
    # 1. ELEMENTOS PRÉ-TEXTUAIS: CAPA
    # ====================================================
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(100)
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run('ESCOLA BRITÂNICA DE ARTES CRIATIVAS E TECNOLOGIA\n')
    r_inst1.bold = True
    r_inst1.font.name = 'Arial'
    r_inst1.font.size = Pt(12)
    r_inst2 = p_inst.add_run('FORMAÇÃO PROFISSIONAL EM ENGENHARIA DE QUALIDADE DE SOFTWARE')
    r_inst2.bold = True
    r_inst2.font.name = 'Arial'
    r_inst2.font.size = Pt(12)

    # Autor
    p_aut = doc.add_paragraph()
    p_aut.paragraph_format.space_after = Pt(140)
    p_aut.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_aut = p_aut.add_run('LEONARDO DE ALMEIDA')
    r_aut.bold = True
    r_aut.font.name = 'Arial'
    r_aut.font.size = Pt(12)

    # Título do Trabalho
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_after = Pt(180)
    p_tit.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.line_spacing = 1.5
    r_tit = p_tit.add_run('ESTRATÉGIA E IMPLEMENTAÇÃO DE ENGENHARIA DE QUALIDADE DE SOFTWARE PARA A PLATAFORMA EBAC-SHOP\n')
    r_tit.bold = True
    r_tit.font.name = 'Arial'
    r_tit.font.size = Pt(14)
    r_sub = p_tit.add_run('Automação de Testes Multicamadas (UI, API, Mobile e Performance) e Integração Contínua (CI/CD)')
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(12)

    # Local e Data
    p_loc = doc.add_paragraph()
    p_loc.paragraph_format.space_after = Pt(0)
    p_loc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_loc = p_loc.add_run('SÃO PAULO – SP\n2026')
    r_loc.bold = True
    r_loc.font.name = 'Arial'
    r_loc.font.size = Pt(12)

    doc.add_page_break()

    # ====================================================
    # 2. FOLHA DE ROSTO
    # ====================================================
    p_fr_aut = doc.add_paragraph()
    p_fr_aut.paragraph_format.space_before = Pt(0)
    p_fr_aut.paragraph_format.space_after = Pt(120)
    p_fr_aut.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_fr_aut = p_fr_aut.add_run('LEONARDO DE ALMEIDA')
    r_fr_aut.bold = True
    r_fr_aut.font.name = 'Arial'
    r_fr_aut.font.size = Pt(12)

    # Título
    p_fr_tit = doc.add_paragraph()
    p_fr_tit.paragraph_format.space_after = Pt(80)
    p_fr_tit.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fr_tit.paragraph_format.line_spacing = 1.5
    r_fr_tit = p_fr_tit.add_run('ESTRATÉGIA E IMPLEMENTAÇÃO DE ENGENHARIA DE QUALIDADE DE SOFTWARE PARA A PLATAFORMA EBAC-SHOP\n')
    r_fr_tit.bold = True
    r_fr_tit.font.name = 'Arial'
    r_fr_tit.font.size = Pt(14)
    r_fr_sub = p_fr_tit.add_run('Automação de Testes Multicamadas (UI, API, Mobile e Performance) e Integração Contínua (CI/CD)')
    r_fr_sub.font.name = 'Arial'
    r_fr_sub.font.size = Pt(12)

    # Nota de Natureza do Trabalho (Recuo de 8 cm à esquerda)
    p_nota = doc.add_paragraph()
    p_nota.paragraph_format.left_indent = Inches(3.15) # 8.0 cm
    p_nota.paragraph_format.space_after = Pt(140)
    p_nota.paragraph_format.line_spacing = 1.0
    p_nota.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_nota = p_nota.add_run('Trabalho de Conclusão de Curso apresentado à Escola Britânica de Artes Criativas e Tecnologia (EBAC) como requisito parcial para obtenção do certificado de conclusão da Formação Profissional em Engenheiro de Qualidade de Software.\n\nOrientador: Prof. Fábio Araújo')
    r_nota.font.name = 'Arial'
    r_nota.font.size = Pt(10)

    # Local e Ano
    p_fr_loc = doc.add_paragraph()
    p_fr_loc.paragraph_format.space_after = Pt(0)
    p_fr_loc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_fr_loc = p_fr_loc.add_run('SÃO PAULO – SP\n2026')
    r_fr_loc.bold = True
    r_fr_loc.font.name = 'Arial'
    r_fr_loc.font.size = Pt(12)

    doc.add_page_break()

    # ====================================================
    # 3. RESUMO
    # ====================================================
    p_res_title = doc.add_paragraph()
    p_res_title.paragraph_format.space_before = Pt(18)
    p_res_title.paragraph_format.space_after = Pt(18)
    p_res_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rt = p_res_title.add_run('RESUMO')
    r_rt.bold = True
    r_rt.font.name = 'Arial'
    r_rt.font.size = Pt(12)

    add_p(
        'Este Trabalho de Conclusão de Curso apresenta a estratégia e a implementação abrangente de Engenharia de '
        'Qualidade de Software (Quality Engineering - QE) para a plataforma de e-commerce EBAC-SHOP. Adotando a '
        'abordagem Shift-Left Testing e a metodologia BDD (Behavior-Driven Development) com sintaxe Gherkin, '
        'foram especificadas 8 histórias de usuário e estruturada uma matriz analítica de casos de teste com técnicas '
        'formais de Partição de Equivalência, Análise do Valor Limite, Tabela de Decisão e Transição de Estados. '
        'A pirâmide de testes foi operacionalizada de ponta a ponta: testes funcionais E2E de interface web desenvolvidos '
        'em Cypress com aplicação do padrão Page Object Model e relatórios automatizados Mochawesome; testes funcionais '
        'e validação estrita de contratos via JSON Schema (Ajv) para a API REST de Cupons com Supertest e Jest; automação '
        'mobile para aplicativo Android utilizando WebdriverIO e Appium; e testes de carga e desempenho de alta escala '
        'com o framework K6 para 20 usuários virtuais simultâneos sob rígidos critérios de aceitação (SLA). Todos os '
        'testes foram orquestrados em esteiras de Integração Contínua (CI/CD) via GitHub Actions, garantindo feedback '
        'imediato, rastreabilidade e máxima confiabilidade para o ciclo de entrega de software.',
        space_after=18, first_line_indent=0.0
    )

    add_p('Engenharia de Qualidade de Software. Testes Automatizados. BDD. Cypress. Supertest. K6. CI/CD. GitHub Actions.', bold_prefix='Palavras-chave: ', space_after=0, first_line_indent=0.0)

    doc.add_page_break()

    # ====================================================
    # 4. SUMÁRIO ABNT NBR 6027
    # ====================================================
    p_sum_title = doc.add_paragraph()
    p_sum_title.paragraph_format.space_before = Pt(18)
    p_sum_title.paragraph_format.space_after = Pt(18)
    p_sum_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_st = p_sum_title.add_run('SUMÁRIO')
    r_st.bold = True
    r_st.font.name = 'Arial'
    r_st.font.size = Pt(12)

    sumario_items = [
        ('1', 'INTRODUÇÃO', '5', 0, True),
        ('1.1', 'Contexto e Motivação', '5', 1, False),
        ('1.2', 'Objetivos do Trabalho', '5', 1, False),
        ('1.3', 'Estrutura do Documento', '5', 1, False),
        ('2', 'ESTRATÉGIA DE TESTES E ENGENHARIA DE QUALIDADE', '6', 0, True),
        ('2.1', 'Objetivos de Qualidade e Governança', '6', 1, False),
        ('2.2', 'Papéis e Responsabilidades no Time Ágil', '6', 1, False),
        ('2.3', 'Pirâmide de Testes e Abordagem Shift-Left', '6', 1, False),
        ('2.4', 'Técnicas de Design de Testes Aplicadas', '7', 1, False),
        ('2.5', 'Mapa Mental da Estratégia de Qualidade', '7', 1, False),
        ('3', 'ESPECIFICAÇÃO DE REQUISITOS E BDD (GHERKIN)', '8', 0, True),
        ('3.1', 'Metodologia BDD e Especificação por Exemplos', '8', 1, False),
        ('3.2', 'Histórias de Usuário e Critérios de Aceitação', '8', 1, False),
        ('4', 'MATRIZ DE RASTREABILIDADE E CASOS DE TESTE', '11', 0, True),
        ('4.1', 'Mapeamento de Cobertura e Relação com Técnicas Formais', '11', 1, False),
        ('5', 'IMPLEMENTAÇÃO DOS TESTES AUTOMATIZADOS', '13', 0, True),
        ('5.1', 'Repositório Oficial no GitHub e Estrutura de Código', '13', 1, False),
        ('5.2', 'Automação de Interface Web (Cypress + Page Object Model)', '13', 1, False),
        ('5.3', 'Automação de API REST e Validação de Contrato (Supertest + Ajv)', '14', 1, False),
        ('5.4', 'Automação Mobile Android (WebdriverIO + Appium)', '15', 1, False),
        ('5.5', 'Testes de Performance e Carga (K6)', '15', 1, False),
        ('6', 'INTEGRAÇÃO CONTÍNUA (CI/CD VIA GITHUB ACTIONS)', '16', 0, True),
        ('6.1', 'Arquitetura e Automação de Pipelines', '16', 1, False),
        ('7', 'CONCLUSÃO E LIÇÕES APRENDIDAS', '17', 0, True),
        ('8', 'REFERÊNCIAS BIBLIOGRÁFICAS', '18', 0, True)
    ]

    for num, title_text, page_num, level, is_bold in sumario_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(2)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.15
        
        indent = "    " * level
        item_text = f"{indent}{num} {title_text}" if num else f"{indent}{title_text}"
        
        # Leader dots
        dots_count = max(2, 68 - len(item_text) - len(page_num))
        dots = ' .' * (dots_count // 2)
        
        r_txt = p_item.add_run(item_text + dots + ' ' + page_num)
        r_txt.font.name = 'Arial'
        r_txt.font.size = Pt(11)
        r_txt.bold = is_bold

    # ====================================================
    # NOVA SEÇÃO: ELEMENTOS TEXTUAIS (COM NUMERAÇÃO DE PÁGINA)
    # ====================================================
    sec_body = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_body.top_margin = Inches(1.18)
    sec_body.bottom_margin = Inches(0.79)
    sec_body.left_margin = Inches(1.18)
    sec_body.right_margin = Inches(0.79)
    sec_body.header.is_linked_to_previous = False
    
    header_para = sec_body.header.paragraphs[0]
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = header_para.add_run()
    hrun.font.name = 'Arial'
    hrun.font.size = Pt(10)
    add_page_number(hrun)

    # ----------------------------------------------------
    # 1. INTRODUÇÃO
    # ----------------------------------------------------
    add_sec_title('INTRODUÇÃO', '1')
    
    add_subsec_title('Contexto e Motivação', '1.1')
    add_p('No cenário dinâmico do comércio eletrônico contemporâneo, a estabilidade funcional, a segurança das transações e a performance sob tráfego concorrente constituem fatores determinantes para o sucesso do negócio e a fidelização de clientes. Falhas em fluxos críticos, tais como autenticação de usuários, gerenciamento do carrinho de compras e validação de cupons promocionais, impactam diretamente a receita e comprometem a reputação institucional.')
    add_p('Nesse contexto, a transição da tradicional garantia de qualidade (QA) para a Engenharia de Qualidade de Software (Quality Engineering - QE) estabelece uma abordagem proativa e preventiva. A prática de Shift-Left Testing possibilita a inserção das diretrizes de qualidade desde a concepção dos requisitos, viabilizando a identificação precoce de inconsistências e otimizando o custo de correção ao longo do ciclo de vida de desenvolvimento.')

    add_subsec_title('Objetivos do Trabalho', '1.2')
    add_p('Este trabalho tem como objetivo principal projetar, documentar e implementar uma arquitetura completa de testes automatizados e integração contínua para a plataforma de e-commerce EBAC-SHOP (hospedada em ambiente simulado e conteinerizado via Docker).')
    add_p('Especificamente, buscou-se alcançar os seguintes objetivos operacionais:')
    add_p('1. Especificar cenários de negócio utilizando Behavior-Driven Development (BDD) e sintaxe Gherkin para 8 histórias de usuário;', first_line_indent=0.49, space_after=3)
    add_p('2. Estruturar matriz de testes aplicando técnicas de caixa-preta (Partição de Equivalência, Análise do Valor Limite e Tabela de Decisão);', first_line_indent=0.49, space_after=3)
    add_p('3. Implementar suíte de testes de ponta a ponta (E2E) para interface web utilizando Cypress e padrão Page Objects;', first_line_indent=0.49, space_after=3)
    add_p('4. Desenvolver suíte de testes de integração e contrato de API RESTful utilizando Supertest, Jest e validação JSON Schema com Ajv;', first_line_indent=0.49, space_after=3)
    add_p('5. Implementar automação de testes para aplicativo móvel Android utilizando WebdriverIO e Appium;', first_line_indent=0.49, space_after=3)
    add_p('6. Avaliar a resiliência e o desempenho da infraestrutura com testes de carga automatizados via K6 sob metas de SLA estritas;', first_line_indent=0.49, space_after=3)
    add_p('7. Orquestrar a execução de todas as baterias de testes em pipelines automatizados de CI/CD utilizando GitHub Actions.', first_line_indent=0.49, space_after=6)

    add_subsec_title('Estrutura do Documento', '1.3')
    add_p('O presente documento está organizado da seguinte forma: a Seção 2 delineia a Estratégia de Testes e governança de qualidade; a Seção 3 apresenta os Critérios de Aceitação modelados em BDD/Gherkin; a Seção 4 expõe a Matriz de Casos de Teste e rastreabilidade técnica; a Seção 5 detalha a Implementação dos Testes Automatizados (Web, API, Mobile e Performance); a Seção 6 descreve a pipeline de CI/CD via GitHub Actions; e a Seção 7 conclui o trabalho com os resultados e considerações finais.')

    # ----------------------------------------------------
    # 2. ESTRATÉGIA DE TESTES
    # ----------------------------------------------------
    add_sec_title('ESTRATÉGIA DE TESTES E ENGENHARIA DE QUALIDADE', '2')
    
    add_subsec_title('Objetivos de Qualidade e Governança', '2.1')
    add_p('A estratégia de qualidade do projeto EBAC-SHOP foi concebida para assegurar que a plataforma opere com alta disponibilidade, integridade transacional e precisão lógica. A governança do processo de qualidade apoia-se em critérios objetivos de aceitação (DoD - Definition of Done), garantindo que nenhum incremento seja entregue em produção sem a devida cobertura de testes automatizados.')

    add_subsec_title('Papéis e Responsabilidades no Time Ágil', '2.2')
    add_p('A atuação em equipe ágil distribui as responsabilidades de qualidade de forma colaborativa:', space_after=3)
    add_p('Engenheiro de Qualidade (QE): Responsável pelo planejamento estratégico, modelagem de cenários de teste, arquitetura dos frameworks de automação (Web, API, Mobile, Performance) e configuração dos pipelines de CI/CD.', bold_prefix='• ', first_line_indent=0.49, space_after=3)
    add_p('Desenvolvedores (Devs): Responsáveis pela construção das funcionalidades, garantia de cobertura de testes unitários e adesão aos contratos de API.', bold_prefix='• ', first_line_indent=0.49, space_after=3)
    add_p('Product Owner (PO): Responsável pela definição das regras de negócio, priorização das histórias e validação dos critérios de aceitação junto aos stakeholders.', bold_prefix='• ', first_line_indent=0.49, space_after=6)

    add_subsec_title('Pirâmide de Testes e Abordagem Shift-Left', '2.3')
    add_p('Seguindo o modelo conceitual da Pirâmide de Testes de Martin Fowler, a distribuição dos testes foi balanceada para otimizar velocidade de execução e confiabilidade de feedback. A maior densidade de testes concentra-se na camada de serviços/API (validações rápidas e determinísticas), complementada por testes ponta a ponta (E2E) focados nas jornadas críticas de conversão na Web e no Mobile.')

    add_subsec_title('Técnicas de Design de Testes Aplicadas', '2.4')
    add_p('Para assegurar a máxima cobertura lógica com um número otimizado de casos, foram aplicadas quatro técnicas formais de teste de caixa-preta:')
    add_p('Divisão dos domínios de entrada em classes válidas e inválidas (ex.: quantidades de itens no carrinho, cupons válidos e inválidos).', bold_prefix='1. Partição de Equivalência (EP): ', first_line_indent=0.49, space_after=3)
    add_p('Teste dos valores limites nas fronteiras das partições (ex.: limites de 10 e 11 itens por produto; teto de compra de R$ 990,00 e R$ 990,01).', bold_prefix='2. Análise do Valor Limite (BVA): ', first_line_indent=0.49, space_after=3)
    add_p('Mapeamento de combinações lógicas de regras de negócio (ex.: faixas de valor de compra de R$ 200 a R$ 600 gerando 10% de desconto; acima de R$ 600 gerando 15% de desconto; regras de autenticação com usuários ativos e inativos).', bold_prefix='3. Tabela de Decisão: ', first_line_indent=0.49, space_after=3)
    add_p('Validação dos ciclos de vida e bloqueios (ex.: bloqueio temporário de 15 minutos na conta de usuário após 3 tentativas inválidas de autenticação).', bold_prefix='4. Transição de Estados: ', first_line_indent=0.49, space_after=6)

    add_subsec_title('Mapa Mental da Estratégia de Qualidade', '2.5')
    add_p('O diagrama visual a seguir consolida a estrutura metodológica, ferramentas e esteira de qualidade do projeto:')

    img_p = r'C:\Users\leona\TCC-EBAC-QE\docs\mapa-mental-estrategia.png'
    if os.path.exists(img_p):
        p_cap_top = doc.add_paragraph()
        p_cap_top.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap_top.paragraph_format.space_before = Pt(6)
        p_cap_top.paragraph_format.space_after = Pt(2)
        r_ct = p_cap_top.add_run('Figura 1 – Mapa mental da estratégia de testes para a plataforma EBAC-SHOP.')
        r_ct.bold = True
        r_ct.font.size = Pt(10)

        p_i = doc.add_paragraph()
        p_i.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_i.paragraph_format.space_after = Pt(2)
        p_i.add_run().add_picture(img_p, width=Inches(6.0))

        p_cap_bot = doc.add_paragraph()
        p_cap_bot.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap_bot.paragraph_format.space_after = Pt(12)
        r_cb = p_cap_bot.add_run('Fonte: Elaborado pelo autor (2026).')
        r_cb.font.size = Pt(10)

    # ----------------------------------------------------
    # 3. ESPECIFICAÇÃO DE REQUISITOS E BDD (GHERKIN)
    # ----------------------------------------------------
    add_sec_title('ESPECIFICAÇÃO DE REQUISITOS E BDD (GHERKIN)', '3')
    
    add_subsec_title('Metodologia BDD e Especificação por Exemplos', '3.1')
    add_p('A adoção do BDD promove a colaboração entre as equipes de negócios, desenvolvimento e testes por meio de uma linguagem comum, estruturada no padrão Dado-Quando-Então (Given-When-Then). As 8 histórias de usuário foram integralmente refinadas nesse modelo.')

    add_subsec_title('Histórias de Usuário e Critérios de Aceitação', '3.2')
    
    with open(r'C:\Users\leona\TCC-EBAC-QE\docs\estrategia-e-casos-de-teste.md', 'r', encoding='utf-8') as f_md:
        md_text = f_md.read()

    us_blocks = re.findall(r'(### \[US-\d+\].*?)(?=### \[US-|\Z)', md_text, re.DOTALL)
    for us in us_blocks:
        lines = us.strip().split('\n')
        title = lines[0].replace('### ', '').strip()
        add_subsubsec_title(title)
        
        # User story text
        desc_lines = [l for l in lines[1:5] if l.strip().startswith('**')]
        if desc_lines:
            add_p(' '.join(desc_lines).replace('**', ''), first_line_indent=0.0, space_after=4)
        
        code_match = re.search(r'```gherkin(.*?)```', us, re.DOTALL)
        if code_match:
            add_code_block(code_match.group(1).strip())

    # ----------------------------------------------------
    # 4. MATRIZ DE RASTREABILIDADE E CASOS DE TESTE
    # ----------------------------------------------------
    add_sec_title('MATRIZ DE RASTREABILIDADE E CASOS DE TESTE', '4')
    
    add_subsec_title('Mapeamento de Cobertura e Relação com Técnicas Formais', '4.1')
    add_p('A matriz de rastreabilidade a seguir correlaciona cada caso de teste com a história de usuário de origem, o tipo de fluxo avaliado, a técnica de design de teste empregada e o status de automação na suíte:')

    p_tbl_title = doc.add_paragraph()
    p_tbl_title.paragraph_format.space_before = Pt(6)
    p_tbl_title.paragraph_format.space_after = Pt(2)
    p_tbl_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tt = p_tbl_title.add_run('Tabela 1 – Matriz de casos de teste, técnicas aplicadas e status de automação.')
    r_tt.bold = True
    r_tt.font.size = Pt(10)

    table_cases = [
        ('TC-001', 'US-0001', 'Adicionar 10 itens de um mesmo produto', 'Caminho Feliz', 'Valor Limite (BVA)', 'Sim (UI)'),
        ('TC-002', 'US-0001', 'Tentar adicionar 11 itens de um produto', 'Caminho Negativo', 'Valor Limite (BVA)', 'Sim (UI)'),
        ('TC-003', 'US-0001', 'Bloquear checkout com valor total > R$ 990', 'Caminho Negativo', 'Partição Equivalência', 'Sim (UI)'),
        ('TC-004', 'US-0001', 'Aplicar cupom 10% (R$ 200 a R$ 600)', 'Caminho Alternativo', 'Tabela de Decisão', 'Sim (UI)'),
        ('TC-005', 'US-0001', 'Aplicar cupom 15% (acima de R$ 600)', 'Caminho Alternativo', 'Tabela de Decisão', 'Não (Manual)'),
        ('TC-006', 'US-0002', 'Login com credenciais válidas de usuário ativo', 'Caminho Feliz', 'Tabela de Decisão', 'Sim (UI / K6)'),
        ('TC-007', 'US-0002', 'Login com senha incorreta', 'Caminho Negativo', 'Partição Equivalência', 'Sim (UI)'),
        ('TC-008', 'US-0002', 'Bloqueio de conta por 15 min após 3 erros', 'Caminho Alternativo', 'Transição de Estados', 'Sim (UI)'),
        ('TC-009', 'US-0002', 'Login com usuário inativo', 'Caminho Negativo', 'Tabela de Decisão', 'Não (Manual)'),
        ('TC-010', 'US-0003', 'Listar cupons via GET com Basic Auth', 'Caminho Feliz', 'Teste de Contrato', 'Sim (API Supertest)'),
        ('TC-011', 'US-0003', 'Consultar cupom por ID existente', 'Caminho Feliz', 'Partição Equivalência', 'Sim (API Supertest)'),
        ('TC-012', 'US-0003', 'Cadastrar cupom com campos obrigatórios', 'Caminho Feliz', 'Partição Equivalência', 'Sim (API Supertest)'),
        ('TC-013', 'US-0003', 'Tentar cadastrar cupom com código duplicado', 'Caminho Negativo', 'Tabela de Decisão', 'Sim (API Supertest)'),
        ('TC-014', 'US-0003', 'Tentar cadastrar cupom sem campo code', 'Caminho Negativo', 'Valor Limite / Schema', 'Sim (API Supertest)'),
        ('TC-015', 'US-0004', 'Buscar produto por palavra-chave no Mobile', 'Caminho Feliz', 'Partição Equivalência', 'Sim (Mobile)'),
        ('TC-016', 'US-0004', 'Filtrar produtos por categoria no Mobile', 'Caminho Alternativo', 'Partição Equivalência', 'Sim (Mobile)'),
        ('TC-017', 'US-0004', 'Ordenar catálogo por menor preço', 'Caminho Alternativo', 'Caixa-Preta', 'Não (Manual)'),
        ('TC-018', 'US-0004', 'Busca por produto inexistente', 'Caminho Negativo', 'Partição Equivalência', 'Não (Manual)'),
        ('TC-019', 'US-0005', 'Acesso ao dashboard da Minha Conta', 'Caminho Feliz', 'Caixa-Preta', 'Não (Manual)'),
        ('TC-020', 'US-0005', 'Logout e invalidação de sessão', 'Caminho Alternativo', 'Transição de Estados', 'Não (Manual)'),
        ('TC-021', 'US-0006', 'Consultar histórico de pedidos anteriores', 'Caminho Feliz', 'Caixa-Preta', 'Não (Manual)'),
        ('TC-022', 'US-0007', 'Atualizar endereço de faturamento', 'Caminho Feliz', 'Partição Equivalência', 'Não (Manual)'),
        ('TC-023', 'US-0008', 'Alterar senha da conta com senha atual', 'Caminho Feliz', 'Tabela de Decisão', 'Não (Manual)'),
        ('TC-024', 'US-0008', 'Tentativa de alteração com senha atual errada', 'Caminho Negativo', 'Tabela de Decisão', 'Não (Manual)')
    ]

    tbl = doc.add_table(rows=len(table_cases) + 1, cols=6)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ['ID', 'História', 'Cenário / Descrição', 'Tipo', 'Técnica', 'Automação']
    for j, h in enumerate(hdrs):
        c = tbl.cell(0, j)
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="1E293B"/>'.format(nsdecls('w'))))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(table_cases):
        for j, val in enumerate(row):
            c = tbl.cell(i + 1, j)
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            if i % 2 == 1:
                c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            r = p.add_run(val)
            r.font.name = 'Arial'
            r.font.size = Pt(8.0)
            if j == 5 and 'Sim' in val:
                r.bold = True
                r.font.color.rgb = RGBColor(22, 101, 52)

    p_tbl_src = doc.add_paragraph()
    p_tbl_src.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_src.paragraph_format.space_before = Pt(2)
    p_tbl_src.paragraph_format.space_after = Pt(12)
    r_ts = p_tbl_src.add_run('Fonte: Elaborado pelo autor (2026).')
    r_ts.font.size = Pt(10)

    # ----------------------------------------------------
    # 5. IMPLEMENTAÇÃO DOS TESTES AUTOMATIZADOS
    # ----------------------------------------------------
    add_sec_title('IMPLEMENTAÇÃO DOS TESTES AUTOMATIZADOS', '5')
    
    add_subsec_title('Repositório Oficial no GitHub e Estrutura de Código', '5.1')
    add_p('O código-fonte integral, suítes de testes, massa de dados e arquivos de automação encontram-se hospedados publicamente no repositório:')
    add_p('https://github.com/leuuh/TCC-EBAC-QE', bold_prefix='Repositório Oficial: ')
    add_p('A estrutura do projeto encontra-se particionada modularmente por camadas tecnológicas, conforme abaixo:')
    add_code_block('TCC-EBAC-QE/\n├── .github/workflows/    # Pipelines de CI/CD (GitHub Actions)\n├── UI/                   # Automação Web E2E (Cypress + Page Objects)\n├── API/                  # Automação de API REST e Contrato (Supertest + Jest + Ajv)\n├── Mobile/               # Automação Mobile Android (WebdriverIO + Appium)\n├── Performance/          # Testes de Carga e Estresse (K6)\n└── docs/                 # Documentação técnica e Diagramas')

    add_subsec_title('Automação de Interface Web (Cypress + Page Object Model)', '5.2')
    add_p('Para a automação dos testes de interface gráfica, foi adotado o Cypress com JavaScript. O framework foi escolhido pela sua execução nativa e direta no navegador, recurso de auto-waiting (mitigando flaky tests), facilidade de relatórios com Mochawesome e forte integração com o padrão Page Object Model.')
    add_p('A suíte de UI valida de forma automatizada a adição de itens ao carrinho com controle de quantidades limites (TC-001 e TC-002), o bloqueio de compras acima do teto de R$ 990,00 (TC-003), a aplicação de cupom de 10% (TC-004), o login com sucesso (TC-006), a rejeição de credenciais inválidas (TC-007) e o bloqueio de conta por tentativas consecutivas incorretas (TC-008).')

    add_subsec_title('Automação de API REST e Validação de Contrato (Supertest + Ajv)', '5.3')
    add_p('A camada de API (/wc/v3/coupons) foi automatizada em Node.js utilizando Supertest e Jest, associados ao validador de contratos Ajv (JSON Schema Draft-07). A suíte executa testes funcionais de métodos HTTP (GET, POST), regras de unicidade de cupons e verificação estrita de tipagem e formato das propriedades dos contratos.')
    add_code_block('PASS tests/coupons.test.js (12.22 s)\n  [US-0003] Suíte de Testes da API de Cupons - EBAC Shop\n    GET /wc/v3/coupons (Listagem de Cupons)\n      ✓ TC-010: Deve listar todos os cupons cadastrados com sucesso (200 OK)\n    POST /wc/v3/coupons (Cadastro de Cupons)\n      ✓ TC-012: Deve cadastrar um cupom com sucesso preenchendo campos obrigatórios\n      ✓ TC-013: Deve rejeitar o cadastro de cupom com código já existente\n      ✓ TC-014: Deve rejeitar cadastro de cupom sem campo obrigatório\n    GET /wc/v3/coupons/:id (Consulta de Cupom por ID)\n      ✓ TC-011: Deve buscar os detalhes de um cupom existente por ID\n      ✓ TC-011-NEG: Deve retornar 404 ao consultar cupom com ID inexistente\n\nPASS tests/contract.test.js\n  [US-0003] Validação de Contrato da API de Cupons (JSON Schema)\n    ✓ TC-010-CONTRACT: O payload deve validar estritamente com o Schema JSON\n\nTest Suites: 2 passed, 2 total | Tests: 7 passed, 7 total (100% de sucesso)')

    add_subsec_title('Automação Mobile Android (WebdriverIO + Appium)', '5.4')
    add_p('A camada mobile valida o aplicativo Android da EBAC Shop via WebdriverIO e Appium com o driver UiAutomator2. A suíte automatiza cenários de busca de produtos por palavra-chave (TC-015), filtragem por categorias de vestuário (TC-016) e navegação detalhada de produtos com padrão Page Object Model.')

    add_subsec_title('Testes de Performance e Carga (K6)', '5.5')
    add_p('Para atestar a estabilidade e capacidade da aplicação sob tráfego concorrente, foram desenvolvidos scripts de teste de carga utilizando a ferramenta Grafana K6. Os cenários simularam 20 Usuários Virtuais (VUs) simultâneos com período de Ramp-Up de 20 segundos e sustentação de 2 minutos sobre os fluxos de vitrine, carrinho e login (utilizando massa de dados parametrizada em JSON).')
    add_p('Os critérios de aceite técnico (SLA) exigiram que 95% das requisições respondessem em tempo inferior a 2000 ms (p95 < 2.0s) e que a taxa de erro fosse estritamente inferior a 5% (error_rate < 0.05), objetivos alcançados com 100% de conformidade.')

    # ----------------------------------------------------
    # 6. INTEGRAÇÃO CONTÍNUA (CI/CD)
    # ----------------------------------------------------
    add_sec_title('INTEGRAÇÃO CONTÍNUA (CI/CD VIA GITHUB ACTIONS)', '6')
    
    add_subsec_title('Arquitetura e Automação de Pipelines', '6.1')
    add_p('Implementou-se uma esteira robusta de Integração Contínua configurada no GitHub Actions (.github/workflows/), estruturada em três fluxos automatizados:')
    add_p('Disparado a cada push e pull request direcionados à branch main, executa a suíte de testes de API e contratos de forma isolada e emite relatório instantâneo de conformidade.', bold_prefix='1. Workflow de API (test-api.yml): ', first_line_indent=0.49, space_after=3)
    add_p('Executa os testes E2E do Cypress em modo headless dentro de container Docker, armazenando artefatos e vídeos de evidência em caso de falha.', bold_prefix='2. Workflow de UI (test-ui.yml): ', first_line_indent=0.49, space_after=3)
    add_p('Execução periódica e sob demanda dos scripts de carga K6 com validação automática dos limiares de SLA estabelecidos.', bold_prefix='3. Workflow de Performance (test-k6.yml): ', first_line_indent=0.49, space_after=6)

    # ----------------------------------------------------
    # 7. CONCLUSÃO
    # ----------------------------------------------------
    add_sec_title('CONCLUSÃO E LIÇÕES APRENDIDAS', '7')
    add_p('A realização deste Trabalho de Conclusão de Curso consolidou os conhecimentos teóricos e práticos adquiridos ao longo da formação em Engenheiro de Qualidade de Software na EBAC. A experiência demonstrou que a atuação do Engenheiro de Qualidade transcende a execução de testes reativos, posicionando-se como um pilar estratégico de sustentabilidade e confiabilidade técnica.')
    add_p('A aplicação das técnicas formais de teste (Partição de Equivalência, Análise do Valor Limite, Tabela de Decisão e Transição de Estados) em conjunto com a metodologia BDD/Gherkin garantiu clareza nos requisitos e preveniu defeitos antes mesmo do início da codificação. A construção de uma pirâmide de testes sólida em múltiplas camadas (UI, API, Mobile, Performance) e sua automação contínua via GitHub Actions proporcionaram uma rede de segurança essencial para deploys contínuos com alta qualidade.')

    # ----------------------------------------------------
    # 8. REFERÊNCIAS
    # ----------------------------------------------------
    add_sec_title('REFERÊNCIAS BIBLIOGRÁFICAS', '8')
    refs = [
        'CRISPIN, Lisa; GREGORY, Janet. Agile Testing: A Practical Guide for Testers and Agile Teams. Boston: Addison-Wesley, 2009.',
        'CYPRESS.IO. Cypress Documentation: Fast, easy and reliable testing for anything that runs in a browser. Disponível em: <https://docs.cypress.io>. Acesso em: 31 ago. 2026.',
        'FOWLER, Martin. Test Pyramid. martinfowler.com, 2012. Disponível em: <https://martinfowler.com/bliki/TestPyramid.html>. Acesso em: 31 ago. 2026.',
        'GRAFANA K6. K6 Documentation: Open-source load testing tool for engineering teams. Grafana Labs, 2026. Disponível em: <https://k6.io/docs/>. Acesso em: 31 ago. 2026.',
        'INTERNATIONAL SOFTWARE TESTING QUALIFICATIONS BOARD (ISTQB). Certified Tester Foundation Level (CTFL) Syllabus v4.0. ISTQB, 2023.',
        'NORTH, Dan. Introducing BDD: What is in a story? Better Software Magazine, 2006. Disponível em: <https://dannorth.net/introducing-bdd/>. Acesso em: 31 ago. 2026.',
        'PRESSMAN, Roger S.; MAXIM, Bruce R. Engenharia de Software: Uma Abordagem Profissional. 9. ed. Porto Alegre: AMGH, 2021.',
        'SOMMERVILLE, Ian. Engenharia de Software. 10. ed. São Paulo: Pearson Education do Brasil, 2019.',
        'WEBDRIVERIO. WebdriverIO: Next-gen browser and mobile automation test framework for Node.js. OpenJS Foundation, 2026. Disponível em: <https://webdriver.io/docs/gettingstarted>. Acesso em: 31 ago. 2026.'
    ]
    for ref in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(8)
        p_r.paragraph_format.line_spacing = 1.0
        p_r.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_r = p_r.add_run(ref)
        r_r.font.name = 'Arial'
        r_r.font.size = Pt(10)

    out_tcc = r'C:\Users\leona\TCC-EBAC-QE\Trabalho de conclusao - Engenheiro de Qualidade de software.docx'
    out_dl = r'C:\Users\leona\Downloads\Trabalho de conclusao - Engenheiro de Qualidade de software_PREENCHIDO.docx'
    doc.save(out_tcc)
    try:
        doc.save(out_dl)
    except Exception:
        pass
    print('Documento TCC ABNT gerado com sucesso em:', out_tcc)

if __name__ == '__main__':
    create_tcc_document()
