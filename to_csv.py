import pandas as pd
import requests
from tqdm.auto import tqdm
from io import StringIO
from Bio.PDB import PDBParser, PPBuilder


data = {
    'pdb_id': [],
    'chain_id_1': [],
    'chain_id_2': [],
    'protein_1': [],
    'protein_2': [],
    'kd': [],
    'pkd': [],
    'method': [],
    'ph': [],
    'temperature': [],
    'reference': [],
    'type': []
}

# Complete dataset from Corrected_Benchmark1.0.pdf https://github.com/haddocking/binding-affinity-benchmark/blob/master/Corrected_Benchmark1.0.pdf
raw_data = [
    ['7CEI', 'A', 'B', 'Colicin E7 nuclease', 'Im7 immunity protein', '5.0 x 10-15', '14.30', 'F', '7.0', '25', 'Keeble et al. (2006) Biochemistry 3243.', 'E'],
    ['1DFJ', 'E', 'I', 'Ribonuclease A', 'Rnase inhibitor', '5.9 x 10-14', '13.23', 'B', '6.0', '25', 'Vincentini et al. (1990) Biochemistry 8827.', 'E'],
    ['1BVN', 'P', 'T', 'α-amylase', 'Tendamistat', '9 x 10-12', '11.05', 'D', '7.0', '25', 'Piervincenzi and Chilkoti (2004) Biomol Eng 21:33.', 'E'],
    ['1IQD', 'AB', 'C', 'Fab', 'Factor VIII domain C2', '1.4 x 10-11', '10.85', 'D', '5.0', '25', 'Jacquemin et al. (1998) Blood 92:496.', 'AB'],
    ['1MAH', 'A', 'F', 'Acetylcholinesterase', 'Fasciculin 2', '2.5 x 10-11', '10.6', 'C', '7.5', '25', 'Marchot et al. (1993) J Biol Chem 12458.', 'E'],
    ['1EZU', 'C', 'AB', 'D102N Trypsin', 'Y69F D70P Ecotin', '8.0 x 10-11', '10.10', 'E', '8.0', '25', 'Yang and Craik (1998) J Mol Biol 1001.', 'E'],
    ['1JPS', 'HL', 'T', 'Fab D3H44', 'Tissue factor', '1.0 x 10-10', '10.00', 'D', '7.4', '25', 'Presta et al. (2001) Thromb Haem 3:379.', 'A'],
    ['1IBR', 'A', 'B', 'Ran GTPase', 'Importin β', '3.0 x 10-10', '9.52', 'C', '7.4', '25', 'Görlich et al. (1996) EMBO 5584.', 'O'],
    ['1R0R', 'A', 'C', 'Subtilisin Carlsberg', 'OMTKY', '3.4 x 10-10', '9.47', 'F', '8.3', '21', 'Horn et al. (2003) J Mol Biol 331:497.', 'E'],
    ['1T6B', 'X', 'Y', 'Anthrax protective antigen', 'Anthrax toxin receptor', '4.0 x 10-10', '9.40', 'D', '7.4', '25', 'Wigdelsworth et al. (2004) J Biol Chem 23349.', 'O'],
    ['1KXP', 'A', 'D', 'Actin', 'Vitamin D binding protein', '1.0 x 10-9', '9.00', 'C', '7.5', '25', 'McLeod et al. (1989) J Biol Chem 1260.', 'O'],
    ['2FD6', 'HL', 'U', 'Urokinase plasminogen receptor antibody', 'Urokinase plasminogen activator receptor', '1.0 x 10-9', '9.00', 'C', '7.4', '23', 'Appella et al (1987) J Biol Chem 4437.', 'A'],
    ['2I25', 'N', 'L', 'Shark single domain antigen receptor', 'Lysozyme', '1.0 x 10-9', '9.00', 'D', '7.4', '25', 'Dooley et al. (2006) PNAS 1846.', 'A'],
    ['2B42', 'A', 'B', 'Xylanase', 'Xylanase inhibitor', '1.07 x 10-9', '8.97', 'D', '5.0', '22', 'Fierens et al (2005) Febs J 5872.', 'E'],
    ['2JEL', 'HL', 'P', 'Fab Jel42', 'HPr', '2.8 x 10-9', '8.55', 'A', '7.2', '23', 'Smallshaw et al. (1998) J Mol Biol 280:765.', 'AB'],
    ['1ML0', 'ABC', 'H', 'Hpr Kinase C-ter domain', 'HPr', '3.1 x 10-9', '8.51', 'D', '8.0', '25', 'Lavergne (2002) Biochemistry 41(20):6218.', 'E'],
    ['1BJ1', 'HL', 'VW', 'Fab', 'vEGF', '3.4 x 10-9', '8.47', 'D', '7.4', '25', 'Muller et al. (1998) Structure 6(9):1153.', 'AB'],
    ['1KXQ', 'H', 'A', 'Camel VHH', 'Pancreatic α-amylase', '3.5 x 10-9', '8.46', 'D', '7.4', '25', 'Lauwereys et al. (1998) EMBO 13:3512.', 'AB'],
    ['1OPH', 'A', 'B', 'α-1-antitrypsin', 'Trypsinogen', '5 x 10-9', '8.30', 'A', '7.4', '25', 'Stratikos and Gettins (1997) PNAS 94:453.', 'E'],
    ['1M10', 'A', 'B', 'Von Willebrand Factor Domain A1', 'Glycoprotein IB-α', '5.8 x 10-9', '8.24', 'D', '7.4', '25', 'Huizinga et al. (2002) Science 297:1176.', 'E'],
    ['2AJF', 'A', 'E', 'ACE2', 'SARS spike protein receptor binding domain', '1.62 x 10-8', '7.79', 'D', '7.4', '25', 'Li et al. (2005) EMBO 24:1634.', 'O'],
    ['1IJK', 'A', 'BC', 'Von Willebrand Factor Domain A1', 'Botrocetin', '2.3 x 10-8', '7.64', 'C', '7.4', '25', 'Miura et al. (2000) J Biol Chem 7539.', 'E'],
    ['1H1V', 'A', 'G', 'Actin', 'Gelsonin', '2.3 x 10-8', '7.64', 'B', '7.0', '20', 'Kinosian et al. (1996) Biochemistry 16550.', 'O'],
    ['1E6J', 'HL', 'P', 'Fab', 'HIV-1 capsid protein 24', '2.9 x 10-8', '7.53', 'D', '7.4', '25', 'Monaco-Malbet et al. (2000) Structure 8:1069.', 'A'],
    ['2HLE', 'A', 'B', 'Ephrin B4 receptor', 'Ephrin B2 ectodomain', '4.0 x 10-8', '7.40', 'F', '7.8', '25', 'Chrencik et al. (2006) J Biol Chem 28185.', 'O'],
    ['1A2K', 'C', 'AB', 'Ran GTPase', 'Nuclear Transport Factor 2', '1 x 10-7', '7.00', 'F', '7.5', '25', 'Chaillan-Huntington et al. (2000) J Biol Chem 5874.', 'O'],
    ['2C0L', 'A', 'B', 'PTS1 and TRP region of PEX5', 'SCP2', '1.09 x 10-7', '6.96', 'F', '7.4', '35', 'Stanley et al. (2006) Mol Cell 24:653.', 'O'],
    ['1RLB', 'ABCD', 'E', 'Transthyretin', 'Retinol binding protein', '1.34 x 10-7', '6.87', 'A', '7.4', '25', 'Noy et al. (1992) Biochemistry 31:11118.', 'O'],
    ['1GRN', 'A', 'B', 'CDC42 GTPase', 'CDC42 GAP', '3.88 x 10-7', '6.41', 'A', '8.0', '25', 'Hoffman et al. (1998) J Biol Chem 4392.', 'O'],
    ['1E6E', 'A', 'B', 'Adrenoxin reductase', 'Adrenoxin', '0.86 x 10-6', '6.07', 'D', '7.4', '25', 'Schiffler et al. (2004) J Biol Chem 34269.', 'E'],
    ['1J2J', 'A', 'B', 'Arf1 GTPase', 'GAT domain of GGA1', '1.1 x 10-6', '5.96', 'D', '8.0', '25', 'Shiba et al. (2003) Nat Struct Biol 10:386.', 'O'],
    ['2BTF', 'A', 'P', 'Actin', 'Profilin', '2.3 x 10-6', '5.70', 'A', '7.0', '25', 'Schlűter et al. (1998) J Cell Sci 111:3261.', 'O'],
    ['1HE8', 'B', 'A', 'Ras GTPase', 'PIP3 kinase', '2.5 x 10-6', '5.60', 'A', '7.5', '20', 'Pacold et al. (2000) Cell 103:931.', 'O'],
    ['1B6C', 'A', 'B', 'FKBP Binding Protein', 'TGFβ receptor', '2.8 x 10-6', '5.55', 'D', '7.4', '25', 'Huse et al. (2001) Mol Cell 8:671.', 'O'],
    ['1I4D', 'D', 'AB', 'Rac GTPase', 'Arfaptin', '3 x 10-6', '5.52', 'F', '8.7', '22', 'Tarricone et al. (2001) Nature 411:215.', 'O'],
    ['1GHQ', 'A', 'B', 'Complement C3', 'Epstein-Barr virus receptor CR2', '4.3 x 10-6', '5.37', 'D', '7.4', '25', 'Sarrias et al. (2001) J Immun 167:1490.', 'O'],
    ['2MTA', 'HL', 'A', 'Methylamine Dehydrogenase', 'Amicyanin', '4.5 x 10-6', '5.35', 'G', '7.5', '25', 'Davidson et al. (1993) BBA 1144:39.', 'E'],
    ['1E96', 'A', 'B', 'Rac GTPase', 'p67 Phox', '6 x 10-6', '5.22', 'F', '7.0', '18', 'Lapouge et al. (2000) Mol Cell 6:899.', 'O'],
    ['1Z0K', 'A', 'B', 'Rab4A GTPase', 'RAB4 binding domain of Rabenosyn', '7.2 x 10-6', '5.14', 'D', '7.5', '25', 'Eathiraj et al. (2005) Nature 436:415.', 'O'],
    ['1QA9', 'A', 'B', 'CD2', 'CD58', '9 x 10-6', '5.05', 'D', '7.4', '37', 'van der Merwe et al. (1994) Biochemistry 10149.', 'O'],
    ['1AK4', 'A', 'D', 'Cyclophilin', 'HIV capsid', '1.60 x 10-5', '4.80', 'F', '6.5', '20', 'Yoo et al. (1997) J Mol Biol 269:780.', 'O'],
    ['1GCQ', 'B', 'C', 'GRB2 C-ter SH3 domain', 'GRB2 N-ter SH3 domain', '1.68 x 10-5', '4.77', 'D', '7.4', '25', 'Nishida et al. (2001) EMBO 20:2995.', 'O'],
    ['1WQ1', 'R', 'G', 'Ras GTPase', 'Ras GAP', '1.7 x 10-5', '4.77', 'B', '7.5', '25', 'Eccleston et al. (1993) J Biol Chem 27012.', 'O'],
    ['2OOB', 'A', 'B', 'Ubiquitin ligase', 'Ubiquitin', '6.0 x 10-5', '4.22', 'F', '7.0', '25', 'Kozlov et al (2007) J Biol Chem 35787.', 'O'],
    ['1AKJ', 'AB', 'DE', 'MHC CLass 1 HLA-A2', 'T-cell CD8 coreceptor', '1.26 x 10-4', '3.90', 'D', '7.4', '25', 'Wyer et all (1999) Immunity 10:219.', 'O'],
    ['1S1Q', 'A', 'B', 'UEV domain', 'Ubiquitin', '6.35 x 10-4', '3.19', 'D', '7.2', '20', 'Pornillos et al (2002), EMBO J 21:2397.', 'O']
]

# Convert to DataFrame
df = pd.DataFrame(raw_data, columns=data.keys())

# Convert kd, pkd, ph and temperature to float
df['kd'] = df['kd'].map(lambda x: float(x.split('x')[0].strip()) * 10 ** -float(x.split('-')[-1].strip()))
df['pkd'] = df['pkd'].astype(float)
df['ph'] = df['ph'].astype(float)
df['temperature'] = df['temperature'].astype(float)


def get_all_chain_sequences(pdb_text):
    """
    Parse the PDB text and return a dictionary mapping each chain ID to its protein sequence.
    We use only the first model (common practice) when multiple models exist.
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("temp", StringIO(pdb_text))
    chain_sequences = {}
    ppb = PPBuilder()
    # Use only the first model to extract chain sequences.
    model = next(structure.get_models())
    for chain in model:
        sequence = ""
        for pp in ppb.build_peptides(chain):
            sequence += str(pp.get_sequence())
        chain_sequences[chain.id] = sequence
    return chain_sequences

new_rows = []

# Process each row in the dataframe
for idx, row in tqdm(df.iterrows(), total=len(df)):
    pdb_id = row['pdb_id']
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    
    response = requests.get(pdb_url)
    if response.status_code == 200:
        pdb_text = response.text
        chain_seqs = get_all_chain_sequences(pdb_text)
        
        # Start with the original row data
        row_dict = row.to_dict()
        # Add each chain's sequence as a new column using the chain ID as the header.
        for chain_id, sequence in chain_seqs.items():
            row_dict[f'chain_{chain_id}'] = sequence
        
        new_rows.append(row_dict)
    else:
        print(f"Warning: Could not download PDB file for {pdb_id}")

# Create a new DataFrame with the original columns plus chain sequence columns.
result_df = pd.DataFrame(new_rows)

# Save the new dataset to a CSV file.
result_df.to_csv("protein_protein_affinity_benchmark.csv", index=False)

print("Done")
