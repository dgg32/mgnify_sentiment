import sys, json, os

top_folder = sys.argv[1]
output_folder = sys.argv[2]

extension = ".json"



desired_rank = "genus"

taboos = ["uncultured_bacterium", "bacterium_enrichment_culture"]




for (head, dirs, files) in os.walk(top_folder):
    for file in files:
        if file.endswith(extension):
            current_file_path = os.path.abspath(os.path.dirname(os.path.join(head, file)))
            with_name = current_file_path + "/"+ file

            sample = file.replace(extension, "")

            category = os.path.dirname(with_name).split("/")[-1]

            #print (category)

            n = 0

            with open(with_name, 'r') as json_file:
                data = json.load(json_file)

                text_form = ""

                for item in data:
                    for name in item:

                        go = True

                        for taboo in taboos:

                            if taboo in name:
                                go = False

                        if go == True:

                            if "count" in item[name] and "rank" in item[name] and item[name]["rank"] == desired_rank:

                                text_form += (name + " ") * int(item[name]["count"])
                                n += 1

                text_form = text_form.strip()

            if len(text_form) > 0 and n >= 20:
                output_sub_folder = os.path.join(output_folder, category)

                if not os.path.isdir(output_sub_folder):
                    os.makedirs(output_sub_folder)

                output_file = os.path.join(output_sub_folder, sample + ".txt")

                with open(output_file, 'w') as out_file:
                    out_file.write(text_form)