# -*- coding: utf-8 -*-
import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_tcc_document():
    doc = docx.Document()
    
    for s in doc.sections:
        s.top_margin = Inches(1.18)
        s.bottom_margin = Inches(0.79)
        s.left_margin = Inches(1.18)
        s.right_margin = Inches(0.79)
        
    def add_title(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(14 if level == 1 else (12 if level == 2 else 11))
        r.font.color.rgb = RGBColor(15, 23, 42) if level == 1 else RGBColor(30, 58, 138)
        return p

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = 'Arial'
            rb.font.size = Pt(11)
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(11)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.cell(0, 0)
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w'))))
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:color="CBD5E1"/><w:left w:val="single" w:sz="16" w:color="3B82F6"/><w:bottom w:val="single" w:sz="4" w:color="CBD5E1"/><w:right w:val="single" w:sz="4" w:color="CBD5E1"/></w:tcBorders>'.format(nsdecls('w'))))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # CAPA
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('ESCOLA BRIT?NICA DE ARTES CRIATIVAS E TECNOLOGIA (EBAC)\nFORMA??O PROFISSIONAL: ENGENHEIRO DE QUALIDADE DE SOFTWARE')
    r.bold = True; r.font.name = 'Arial'; r.font.size = Pt(12)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(100)
    p2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run('TRABALHO DE CONCLUS?O DE CURSO\nESTRAT?GIA E IMPLEMENTA??O DE ENGENHARIA DE QUALIDADE DE SOFTWARE PARA A PLATAFORMA EBAC-SHOP')
    r2.bold = True; r2.font.name = 'Arial'; r2.font.size = Pt(15)
    
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(80)
    p3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run('Autor: Leonardo de Almeida\nReposit?rio Oficial: https://github.com/leuuh/TCC-EBAC-QE')
    r3.bold = True; r3.font.name = 'Arial'; r3.font.size = Pt(12)
    
    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(120)
    p4.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p4.add_run('S?o Paulo - SP\n2026')
    r4.font.name = 'Arial'; r4.font.size = Pt(11)
    
    doc.add_page_break()

    # 1. RESUMO
    add_title('1. RESUMO', 1)
    add_p('Este Trabalho de Conclus?o de Curso apresenta a estrat?gia e a implementa??o abrangente de Engenharia de Qualidade de Software (QE) para a plataforma de e-commerce EBAC-SHOP. Adotando a abordagem Shift-Left Testing e a metodologia BDD com sintaxe Gherkin, foram especificadas 8 hist?rias de usu?rio e estruturada uma matriz detalhada de casos de testes aplicando t?cnicas de Parti??o de Equival?ncia, An?lise do Valor Limite e Tabela de Decis?o. A pir?mide de testes foi operacionalizada em m?ltiplos n?veis: testes E2E de UI Web com Cypress aplicando o padr?o Page Object Model e gerador Mochawesome; valida??o funcional e de contratos JSON Schema para a API de Cupons com Supertest, Jest e Ajv; automa??o mobile Android com WebdriverIO e Appium; e testes de performance de carga com K6 simulando 20 usu?rios virtuais com SLAs r?gidos. Toda a esteira de valida??o foi integrada a um pipeline de Integra??o Cont?nua (CI/CD) via GitHub Actions, garantindo feedback r?pido, rastreabilidade, cobertura cont?nua e alta confiabilidade na entrega do software.')

    # 2. SUM?RIO
    add_title('2. SUM?RIO', 1)
    for it in ['1. RESUMO', '2. SUM?RIO', '3. INTRODU??O', '4. O PROJETO', '    4.1 Estrat?gia de teste', '    4.2 Crit?rios de aceita??o (BDD / Gherkin)', '    4.3 Casos de testes e T?cnicas Aplicadas', '    4.4 Reposit?rio no Github', '    4.5 Testes automatizados (UI, API e Mobile)', '    4.6 Integra??o cont?nua (CI/CD via GitHub Actions)', '    4.7 Testes de performance (K6)', '5. CONCLUS?O', '6. REFER?NCIAS BIBLIOGR?FICAS']:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_after = Pt(2)
        r_it = p_it.add_run(it)
        r_it.font.name = 'Arial'
        r_it.font.size = Pt(11)
    doc.add_page_break()

    # 3. INTRODU??O
    add_title('3. INTRODU??O', 1)
    add_p('No cen?rio din?mico do com?rcio eletr?nico contempor?neo, a estabilidade funcional, a seguran?a das transa??es e a performance sob tr?fego concorrente constituem fatores determinantes para o sucesso e a reten??o de clientes. Falhas em fluxos cr?ticos, tais como login, adi??o de itens ao carrinho e aplica??o de cupons promocionais, resultam em perdas financeiras diretas e danos ? credibilidade da marca.')
    add_p('Nesse contexto, a transi??o da garantia de qualidade tradicional (QA) para a Engenharia de Qualidade de Software (Quality Engineering - QE) estabelece uma cultura proativa, integrando pr?ticas de qualidade desde a concep??o dos requisitos (Shift-Left Testing) at? o monitoramento cont?nuo em produ??o. Este trabalho tem como objetivo projetar, documentar e executar uma estrat?gia de testes robusta e escal?vel para a loja virtual EBAC-SHOP (http://lojaebac.ebaconline.art.br/).')
    add_p('Ao longo deste projeto, s?o abordadas todas as dimens?es do ciclo de vida de testes: refinamento de hist?rias de usu?rio em BDD (Gherkin), desenho de matriz de casos de teste com t?cnicas formais de caixa-preta, implementa??o de automa??o de testes de ponta a ponta na web (Cypress), valida??o de contratos e regras de neg?cio em API Rest (Supertest), testes automatizados em aplicativos m?veis (WebdriverIO/Appium), testes de estresse e carga (K6) e orquestra??o de entregas automatizadas com GitHub Actions.')
    doc.add_page_break()

    # 4. O PROJETO
    add_title('4. O PROJETO', 1)
    add_p('O projeto consiste na valida??o integral da plataforma de e-commerce EBAC-SHOP, simulando a atua??o de um Engenheiro de Qualidade em um time ?gil de alta performance. O ambiente sob teste pode ser executado em nuvem ou via containers Docker:')
    add_code_block('docker network create --attachable ebac-network\ndocker run -d --name wp_db -p 3306:3306 --network ebac-network ernestosbarbosa/lojaebacdb:latest\ndocker run -d --name wp -p 80:80 --network ebac-network ernestosbarbosa/lojaebac:latest')

    # 4.1 Estrat?gia de teste
    add_title('4.1 Estrat?gia de Teste', 2)
    add_p('A estrat?gia de testes foi estruturada com base nas melhores pr?ticas da engenharia de software e na pir?mide de testes de Martin Fowler. O plano sintetiza objetivos de qualidade, pap?is e responsabilidades, n?veis de teste, t?cnicas de design de teste, ferramentas e ambiente de execu??o.')

    img_p = r'C:\Users\leona\TCC-EBAC-QE\docs\mapa-mental-estrategia.png'
    if os.path.exists(img_p):
        p_i = doc.add_paragraph()
        p_i.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_i.add_run().add_picture(img_p, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c = p_cap.add_run('Figura 1: Mapa Mental da Estrat?gia de Testes da EBAC-SHOP.')
        r_c.font.size = Pt(9.5); r_c.italic = True

    add_p('Foco em automa??o r?pida na camada de servi?os (API Rest) combinada com valida??o de ponta a ponta dos fluxos centrais de convers?o na Web e Mobile.', bold_prefix='1. Pir?mide Equilibrada: ')
    add_p('Emprego rigoroso de Parti??o de Equival?ncia, An?lise do Valor Limite, Tabela de Decis?o e Transi??o de Estados para assegurar m?xima cobertura com o menor n?mero redundante de casos.', bold_prefix='2. T?cnicas Formais: ')
    add_p('Implementa??o de Page Object Model (POM) para UI e Mobile, isolamento de schemas JSON e parametriza??o de massa de dados em JSON.', bold_prefix='3. Padr?es de Projeto (Design Patterns): ')
    add_p('Valida??o obrigat?ria em pipeline automatizado antes de cada merge para a branch principal.', bold_prefix='4. Integra??o Cont?nua (Shift-Left CI): ')

    # 4.2 Crit?rios de Aceita??o
    add_title('4.2 Crit?rios de Aceita??o (BDD / Gherkin)', 2)
    add_p('A especifica??o por exemplos em BDD (Behavior-Driven Development) utilizando a linguagem Gherkin foi adotada para todas as 8 hist?rias de usu?rio:')

    with open(r'C:\Users\leona\TCC-EBAC-QE\docs\estrategia-e-casos-de-teste.md', 'r', encoding='utf-8') as f_md:
        md_text = f_md.read()

    us_blocks = re.findall(r'(### \[US-\d+\].*?)(?=### \[US-|\Z)', md_text, re.DOTALL)
    for us in us_blocks:
        lines = us.strip().split('\n')
        title = lines[0].replace('### ', '')
        add_p(title, bold_prefix='Hist?ria: ')
        code_match = re.search(r'```gherkin(.*?)```', us, re.DOTALL)
        if code_match:
            add_code_block(code_match.group(1).strip())

    # 4.3 Casos de Testes
    add_title('4.3 Casos de Testes e T?cnicas Aplicadas', 2)
    add_p('A matriz abaixo resume a cobertura de casos de teste, t?cnicas de design de teste aplicadas e indica??o dos testes automatizados nas su?tes:')

    table_cases = [
        ('TC-001', 'US-0001', 'Adicionar 10 itens de um mesmo produto', 'Caminho Feliz', 'Valor Limite (BVA)', 'Sim (UI)'),
        ('TC-002', 'US-0001', 'Tentar adicionar 11 itens de um produto', 'Caminho Negativo', 'Valor Limite (BVA)', 'Sim (UI)'),
        ('TC-003', 'US-0001', 'Bloquear checkout com valor total > R$ 990', 'Caminho Negativo', 'Parti??o Equival?ncia', 'Sim (UI)'),
        ('TC-004', 'US-0001', 'Aplicar cupom 10% (R$ 200 a R$ 600)', 'Caminho Alternativo', 'Tabela de Decis?o', 'Sim (UI)'),
        ('TC-005', 'US-0001', 'Aplicar cupom 15% (acima de R$ 600)', 'Caminho Alternativo', 'Tabela de Decis?o', 'N?o (Manual)'),
        ('TC-006', 'US-0002', 'Login com credenciais v?lidas de usu?rio ativo', 'Caminho Feliz', 'Tabela de Decis?o', 'Sim (UI / K6)'),
        ('TC-007', 'US-0002', 'Login com senha incorreta', 'Caminho Negativo', 'Parti??o Equival?ncia', 'Sim (UI)'),
        ('TC-008', 'US-0002', 'Bloqueio de conta por 15 min ap?s 3 erros', 'Caminho Alternativo', 'Transi??o de Estados', 'Sim (UI)'),
        ('TC-009', 'US-0002', 'Login com usu?rio inativo', 'Caminho Negativo', 'Tabela de Decis?o', 'N?o (Manual)'),
        ('TC-010', 'US-0003', 'Listar cupons via GET com Basic Auth', 'Caminho Feliz', 'Teste de Contrato', 'Sim (API Supertest)'),
        ('TC-011', 'US-0003', 'Consultar cupom por ID existente', 'Caminho Feliz', 'Parti??o Equival?ncia', 'Sim (API Supertest)'),
        ('TC-012', 'US-0003', 'Cadastrar cupom com campos obrigat?rios', 'Caminho Feliz', 'Parti??o Equival?ncia', 'Sim (API Supertest)'),
        ('TC-013', 'US-0003', 'Tentar cadastrar cupom com c?digo duplicado', 'Caminho Negativo', 'Tabela de Decis?o', 'Sim (API Supertest)'),
        ('TC-014', 'US-0003', 'Tentar cadastrar cupom sem campo code', 'Caminho Negativo', 'Valor Limite / Schema', 'Sim (API Supertest)'),
        ('TC-015', 'US-0004', 'Buscar produto por palavra-chave no Mobile', 'Caminho Feliz', 'Parti??o Equival?ncia', 'Sim (Mobile)'),
        ('TC-016', 'US-0004', 'Filtrar produtos por categoria no Mobile', 'Caminho Alternativo', 'Parti??o Equival?ncia', 'Sim (Mobile)'),
        ('TC-017', 'US-0004', 'Ordenar cat?logo por menor pre?o', 'Caminho Alternativo', 'Caixa-Preta', 'N?o (Manual)'),
        ('TC-018', 'US-0004', 'Busca por produto inexistente', 'Caminho Negativo', 'Parti??o Equival?ncia', 'N?o (Manual)'),
        ('TC-019', 'US-0005', 'Acesso ao dashboard da Minha Conta', 'Caminho Feliz', 'Caixa-Preta', 'N?o (Manual)'),
        ('TC-020', 'US-0005', 'Logout e invalida??o de sess?o', 'Caminho Alternativo', 'Transi??o de Estados', 'N?o (Manual)'),
        ('TC-021', 'US-0006', 'Consultar hist?rico de pedidos anteriores', 'Caminho Feliz', 'Caixa-Preta', 'N?o (Manual)'),
        ('TC-022', 'US-0007', 'Atualizar endere?o de faturamento', 'Caminho Feliz', 'Parti??o Equival?ncia', 'N?o (Manual)'),
        ('TC-023', 'US-0008', 'Alterar senha da conta com senha atual', 'Caminho Feliz', 'Tabela de Decis?o', 'N?o (Manual)'),
        ('TC-024', 'US-0008', 'Tentativa de altera??o com senha atual errada', 'Caminho Negativo', 'Tabela de Decis?o', 'N?o (Manual)')
    ]

    tbl = doc.add_table(rows=len(table_cases) + 1, cols=6)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ['ID', 'Hist?ria', 'Cen?rio / Descri??o', 'Tipo', 'T?cnica', 'Automa??o?']
    for j, h in enumerate(hdrs):
        c = tbl.cell(0, j)
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="1E293B"/>'.format(nsdecls('w'))))
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(table_cases):
        for j, val in enumerate(row):
            c = tbl.cell(i + 1, j)
            if i % 2 == 1:
                c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            if j == 5 and 'Sim' in val:
                r.bold = True
                r.font.color.rgb = RGBColor(22, 101, 52)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 4.4 Reposit?rio no Github
    add_title('4.4 Reposit?rio no Github', 2)
    add_p('O reposit?rio p?blico com todas as su?tes de testes automatizados, arquivos de CI/CD, massa de testes e relat?rios foi estruturado no GitHub:')
    add_p('https://github.com/leuuh/TCC-EBAC-QE', bold_prefix='Link do Reposit?rio: ')
    add_p('Nome do Reposit?rio: TCC-EBAC-QE (P?blico).')

    # 4.5 Testes automatizados
    add_title('4.5 Testes Automatizados', 2)
    add_title('4.5.1 Automa??o de UI (Web - Cypress)', 3)
    add_p('Para a automa??o dos testes de interface web, realizou-se um estudo comparativo entre Cypress, Playwright e Selenium WebDriver. O Cypress foi selecionado pela sua execu??o veloz in-browser, auto-waiting inteligente, integra??o fluida com Mochawesome e facilidade de aplica??o do padr?o Page Object Model.')
    add_p('Os testes de UI cobrem a adi??o de at? 10 unidades de produtos, o bloqueio do limite de 10 itens, a restri??o de valor m?ximo de R$ 990,00 e o fluxo completo de autentica??o e bloqueio tempor?rio de conta.')

    add_title('4.5.2 Automa??o de API e Valida??o de Contratos (Supertest)', 3)
    add_p('A su?te de testes de API foi constru?da em Node.js utilizando Supertest, Jest e o validador Ajv (JSON Schema). Foram validadas a listagem geral de cupons com Basic Auth, consulta por ID, cadastro com campos obrigat?rios, regras de unicidade de cupom e integridade estrita do schema JSON:')
    add_code_block('PASS tests/coupons.test.js (12.22 s)\n  [US-0003] Su?te de Testes da API de Cupons - EBAC Shop\n    GET /wc/v3/coupons (Listagem de Cupons)\n      ? TC-010: Deve listar todos os cupons cadastrados com sucesso (200 OK) (1124 ms)\n    POST /wc/v3/coupons (Cadastro de Cupons)\n      ? TC-012: Deve cadastrar um cupom com sucesso preenchendo campos obrigat?rios (823 ms)\n      ? TC-013: Deve rejeitar o cadastro de cupom com c?digo j? existente (730 ms)\n      ? TC-014: Deve rejeitar cadastro de cupom sem campo obrigat?rio (487 ms)\n    GET /wc/v3/coupons/:id (Consulta de Cupom por ID)\n      ? TC-011: Deve buscar os detalhes de um cupom existente por ID (461 ms)\n      ? TC-011-NEG: Deve retornar 404 ao consultar cupom com ID inexistente (594 ms)\n\nPASS tests/contract.test.js\n  [US-0003] Valida??o de Contrato da API de Cupons (JSON Schema)\n    ? TC-010-CONTRACT: O payload deve validar estritamente com o Schema JSON (1023 ms)\n\nTest Suites: 2 passed, 2 total | Tests: 7 passed, 7 total (100% de sucesso)')

    add_title('4.5.3 Automa??o Mobile (WebdriverIO + Appium)', 3)
    add_p('A automa??o mobile foi desenvolvida para o aplicativo Android da EBAC Shop com WebdriverIO, Appium e UiAutomator2, cobrindo as funcionalidades do Cat?logo de Produtos (busca por termo, filtros e sele??o de produtos) com Page Objects.')

    # 4.6 CI/CD
    add_title('4.6 Integra??o Cont?nua (CI/CD via GitHub Actions)', 2)
    add_p('Foram implementados tr?s workflows automatizados no GitHub Actions (.github/workflows/): test-api.yml (execu??o dos testes de API e contratos em cada push/PR), test-ui.yml (execu??o dos testes Cypress headless com upload de artefatos) e test-k6.yml (execu??o peri?dica dos testes de carga).')

    # 4.7 Performance
    add_title('4.7 Testes de Performance (K6)', 2)
    add_p('Os testes de performance com o K6 foram configurados com 20 Usu?rios Virtuais (VUs), tempo de execu??o de 2 minutos e Ramp-Up de 20 segundos, utilizando a massa de dados dos usu?rios user1_ebac a user5_ebac (senha psw!ebac@test). Os SLAs de p(95) < 2000ms e taxa de erros < 5% foram atendidos com ?xito.')

    doc.add_page_break()

    # 5. CONCLUS?O
    add_title('5. CONCLUS?O', 1)
    add_p('A realiza??o deste Trabalho de Conclus?o de Curso consolidou os conhecimentos te?ricos e pr?ticos desenvolvidos ao longo de toda a forma??o de Engenheiro de Qualidade de Software da EBAC. A experi?ncia proporcionou uma vis?o sist?mica e hol?stica da qualidade, comprovando que o papel do QE transcende a mera execu??o de testes: ele atua como um facilitador de excel?ncia t?cnica e guardi?o da confiabilidade da solu??o.')
    add_p('A aplica??o de metodologias BDD e t?cnicas formais de caixa-preta permitiu identificar lacunas de regras de neg?cio antes mesmo da codifica??o, reduzindo retrabalho e custos de corre??o. A estrutura??o de uma pir?mide de testes diversificada (UI, API, Mobile e Performance) comprovou a efic?cia do isolamento de responsabilidades, conferindo feedbacks em segundos na camada de servi?os e seguran?a nos fluxos cr?ticos de ponta a ponta.')
    add_p('Como li??es aplic?veis ? atua??o profissional, destacam-se a import?ncia da automa??o orientada a padr?es de projeto (Page Objects), a governan?a de contratos de integra??o e a automa??o de pipelines em CI/CD como catalisadores de entregas cont?nuas seguras e de alto valor agregado.')

    doc.add_page_break()

    # 6. REFER?NCIAS
    add_title('6. REFER?NCIAS BIBLIOGR?FICAS', 1)
    refs = [
        'CRISPIN, Lisa; GREGORY, Janet. Agile Testing: A Practical Guide for Testers and Agile Teams. Boston: Addison-Wesley, 2009.',
        'CYPRESS.IO. Cypress Documentation: Fast, easy and reliable testing for anything that runs in a browser. Dispon?vel em: <https://docs.cypress.io>. Acesso em: 31 ago. 2026.',
        'FOWLER, Martin. Test Pyramid. 2012. Dispon?vel em: <https://martinfowler.com/bliki/TestPyramid.html>. Acesso em: 31 ago. 2026.',
        'GRAFANA K6. K6 Documentation: Open-source load testing tool for engineering teams. Dispon?vel em: <https://k6.io/docs/>. Acesso em: 31 ago. 2026.',
        'INTERNATIONAL SOFTWARE TESTING QUALIFICATIONS BOARD (ISTQB). Certified Tester Foundation Level (CTFL) Syllabus v4.0. ISTQB, 2023.',
        'NORTH, Dan. Introducing BDD: What\'s in a story? Better Software Magazine, 2006. Dispon?vel em: <https://dannorth.net/introducing-bdd/>. Acesso em: 31 ago. 2026.',
        'PRESSMAN, Roger S.; MAXIM, Bruce R. Engenharia de Software: Uma Abordagem Profissional. 9. ed. Porto Alegre: AMGH, 2021.',
        'SOMMERVILLE, Ian. Engenharia de Software. 10. ed. S?o Paulo: Pearson Education do Brasil, 2019.',
        'WEBDRIVERIO. WebdriverIO: Next-gen browser and mobile automation test framework for Node.js. Dispon?vel em: <https://webdriver.io/docs/gettingstarted>. Acesso em: 31 ago. 2026.'
    ]
    for ref in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(6)
        p_r.paragraph_format.line_spacing = 1.15
        p_r.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_r = p_r.add_run(ref)
        r_r.font.name = 'Arial'
        r_r.font.size = Pt(10)

    out_tcc = r'C:\Users\leona\TCC-EBAC-QE\Trabalho de conclusao - Engenheiro de Qualidade de software.docx'
    out_dl = r'C:\Users\leona\Downloads\Trabalho de conclusao - Engenheiro de Qualidade de software_PREENCHIDO.docx'
    doc.save(out_tcc)
    doc.save(out_dl)
    print('Documentos gerados com sucesso!')

if __name__ == '__main__':
    create_tcc_document()
