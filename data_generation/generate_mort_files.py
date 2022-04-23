import reformat_files as rf
import os



def merge_splitted_mort_files(mort_files):

	for tup in mort_files:
	
		rf.merge_files(list(tup), "./mortality/" + tup[0].split(sep="/")[-1][:6] + ".txt")



def generate_mort_files_state(state_files, icd, smf=None):

	if icd == 8:
	
		icd_groups = "ICD 69 Groups"
		icd_groups_code = "ICD 69 Groups Code"
		icd_dict_aux = rf.read_dict("ICD8_aux.tsv")
		icd_dict_groups = rf.read_dict("ICD8_recode.tsv")
		file_years = [str(i) for i in range(68,79)]
		years = ["19" + fy for fy in file_years]
		
	elif icd == 9:
	
		icd_groups = "ICD 72 Groups"
		icd_groups_code = "ICD 72 Groups Code"
		icd_dict_aux = rf.read_dict("ICD9_aux.tsv")
		icd_dict_groups = rf.read_dict("ICD9_recode.tsv")
		file_years = [str(i) for i in range(79,99)]
		years = ["19" + fy for fy in file_years]
		
	else:
	
		icd_groups = "ICD 113 Groups"
		icd_groups_code = "ICD 113 Groups Code"
		icd_dict_aux = rf.read_dict("ICD10_aux.tsv")
		icd_dict_groups = rf.read_dict("ICD10_recode.tsv")
		file_years = ["99"] + ["0" + str(i) for i in range(0,10)] + [str(i) for i in range(10,17)]
		years = ["1999"] + ["20" + fy for fy in file_years[1:]]
		
	icd_dict = rf.combine_dicts(icd_dict_aux, icd_dict_groups)
	
	
	rf.delete_sign_files(state_files, "\"")
	rf.delete_comments_files(state_files, "---")
	rf.delete_rows_files(state_files, ["Notes"], ["Total"])
	
	rf.delete_columns_files(
		state_files, 
		["Notes", "State Code", "Race Code", "Gender Code", "Age Group Code", icd_groups, "Population", "Crude Rate"]
	)
	rf.delete_rows_files(state_files, ["Age Group"], ["Not Stated"])
	
	decode_info = {
		"Race": (["Race"], [rf.read_dict("1989-2016_race.tsv")]),
		"Age Group": (["Age Group"], [rf.read_dict("age_groups.tsv")]),
		icd_groups_code: (["ICD Group"], [icd_dict])
	}
	rf.decode_col_files(state_files, decode_info)
	
	if smf: 
	
		merge_splitted_mort_files(smf)
		halves = [mf for sublist in smf for mf in sublist]
		
		for h in halves:
			
			os.remove(h)
		
		state_files = ["./mortality/Mort" + fy + ".txt" for fy in file_years]
		
	if icd == 9:
	
		rf.delete_rows_files(state_files, 4*["Deaths"], [1,2,3,4])


	rf.add_column_files(state_files, ["Year"], [1], [int(y) for y in years])
	rf.merge_files(state_files, "./mortality/state_level/" + "Mort" + str(file_years[0]) + str(file_years[-1]) + ".tsv")
	
	for mf in state_files:
		
		os.remove(mf)



def generate_6816_mort_file(directory):

	common_icd = rf.read_list("./dics_and_lists/ICD_all.tsv")

	fnames = [directory + f for f in os.listdir(directory)]
	fnames_new = [f + "_new" for f in fnames]
	
	rf.cp_files(fnames, fnames_new)
	
	rf.filter_files(fnames_new, ["Race", "ICD Group"], [["White", "Black"], common_icd])
	rf.delete_rows_files(fnames_new, 4*["Deaths"], [1,2,3,4])
	
	rf.merge_files(fnames_new, directory + "Mort6816.tsv")
	
	for fn in fnames_new:
	
		os.remove(fn)



def main():
	
	mort_dir = "./mortality/original_files/"

	mort_files_icd8 = ["./mortality/" + mf for mf in ["Mort" + str(i) + ".txt" for i in range(68,79)]]
	mort_files_icd9 = ["./mortality/" + mf for mf in ["Mort" + str(i) + ".txt" for i in range(79,99)]]
	
	smf1 = [("Mort99_1.txt", "Mort99_2.txt")]
	smf2 = [("Mort0" + i + "_1.txt", "Mort0" + i + "_2.txt") for i in [str(i) for i in range(0,10)]]
	smf3 = [("Mort" + i + "_1.txt", "Mort" + i + "_2.txt") for i in [str(i) for i in range(10,17)]]
	smf = smf1 + smf2 + smf3
	smf = [("./mortality/" + tup[0], "./mortality/" + tup[1]) for tup in smf]
	
	mort_files_icd10 = [mf for sublist in smf for mf in sublist]
	
	state_files = mort_files_icd8 + mort_files_icd9 + mort_files_icd10
	mort_files = state_files + ["./mortality/Mort6878_county.txt", "./mortality/Mort7988_county.txt"]
	org_mort_files = [mort_dir + mf for mf in [m.split(sep="/")[-1] for m in mort_files]]
	
	rf.cp_files(org_mort_files, mort_files)
	
	os.mkdir("./mortality/state_level/")
	generate_mort_files_state(mort_files_icd8, 8)
	generate_mort_files_state(mort_files_icd9, 9)
	generate_mort_files_state(mort_files_icd10, 10, smf=smf)
	
	generate_6816_mort_file("./mortality/state_level/")



if __name__ == '__main__':
    main()
