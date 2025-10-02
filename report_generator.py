#!/usr/bin/env python3
# Report generator - aggregates JSON findings into a single PDF
import os, json, time
from fpdf import FPDF

def gather_reports(path='reports'):
    data = {'recon': [], 'vuln': [], 'collector': []}
    for fname in os.listdir(path):
        if fname.startswith('recon_') and fname.endswith('.json'):
            with open(os.path.join(path, fname)) as f:
                data['recon'].append(json.load(f))
        if fname.startswith('vuln_') and fname.endswith('.json'):
            with open(os.path.join(path, fname)) as f:
                data['vuln'].append(json.load(f))
        if fname.startswith('collector_') and fname.endswith('.json'):
            with open(os.path.join(path, fname)) as f:
                data['collector'].append(json.load(f))
    return data

def make_pdf(output='reports/SentinelAI_Full_Report.pdf'):
    data = gather_reports('reports')
    pdf = FPDF('P','mm','A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.cell(0,10,'SentinelAI - Consolidated Report', ln=True, align='C')
    pdf.ln(6)
    pdf.set_font('Arial','',12)
    pdf.multi_cell(0,6,'This report aggregates recent recon, vulnerability and collection results.')
    pdf.ln(4)
    pdf.set_font('Arial','B',12)
    pdf.cell(0,6,'Recon Summaries:', ln=True)
    pdf.set_font('Arial','',10)
    for r in data.get('recon', []):
        pdf.multi_cell(0,5, f"Scan: {r.get('network')} - found {len(r.get('results', []))} hosts")
    pdf.ln(2)
    pdf.set_font('Arial','B',12)
    pdf.cell(0,6,'Vulnerability Findings:', ln=True)
    pdf.set_font('Arial','',10)
    for v in data.get('vuln', []):
        findings = v.get('findings', [])
        pdf.multi_cell(0,5, f"Findings: {len(findings)}") 
    pdf.output(output)
    print('[Report] PDF generated at', output)

if __name__=='__main__':
    make_pdf()
