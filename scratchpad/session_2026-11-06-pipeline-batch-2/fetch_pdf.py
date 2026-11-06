import sys
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SESS='session_2026-11-06-pipeline-batch-2'
r=rl.fetch('https://idea.ap.buffalo.edu/wp-content/uploads/sites/110/2020/01/AnthropometryofWheeledMobilityProject_FinalReport.pdf',session=SESS,purpose='R10 retrieval of the Anthropometry of Wheeled Mobility Project Final Report (IDeA Center, 2010), the primary document behind the corada.com transcription',timeout=120)
print(type(r))
