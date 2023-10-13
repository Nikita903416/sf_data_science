import os

def clean_sdf(path_to_file):
    """Функиця удаляет все поля из SD файла и добавляет файл с названиями

    Args:
        path_to_file (path): Путь к файлу

    Returns:
        sdf_file, sdf (list, str): Список из строк SD файла и новый SD файл
    """
    with open(path_to_file, "r", errors='replace') as file:
        sdf = list(file)
    
    def list_of_mol(sdf:list) -> list:
        """Функция возвращает SD файл без свойств

        Args:
            sdf (list): Входной SD файл

        Returns:
            new_sdf (list): SD файл без свойств
        """
        new_sdf = []
        temp_mol = []
        
        for row in sdf:
            if row == '$$$$\n':
                temp_mol.append(row)
                temp_mol = temp_mol[0:temp_mol.index('M  END\n')+1]
                new_sdf.append(temp_mol)
                temp_mol = []
            else:
                temp_mol.append(row)
        return new_sdf
    
    
    def fill_sdf(new_sdf: list) -> list:
        """Функция возвращает SD файл с названиями

        Args:
            new_sdf (list): SD файл из list_of_mol

        Returns:
            named_sd_file (list): SD с названиями файлов (уникальными ID соединений)
        """ 
        sdf_witout_props = []
        file_name = path_to_file.split('\\')[-1].replace('.sdf', '')
        prop_name = ">  <NAME>\n"
        database_name = file_name.replace('.sdf', '')
        delim = "\n$$$$\n"
        
        for mol in new_sdf:
            for row in range(0, len(mol)):
                sdf_witout_props.append(mol[row])
                if mol[row] ==  'M  END\n':
                    sdf_witout_props.append(prop_name)
                    name = database_name+"_"+ str(row)+"\n"
                    sdf_witout_props.append(name)
                    sdf_witout_props.append(delim)
        return sdf_witout_props
    
    sdf = list_of_mol(sdf)
    named_sd_file = fill_sdf(sdf)

    return named_sd_file


def sdf_joiner(path_to_dir: str, write_in_file = None) -> list:
    """Функция обединяет все SD файлы из директории

    Args:
        path_to_dir (str): Путь в директорию с файлами
        write_in_file (_type_, optional): Путь к файла для сохранения SD (если None, то файл не сохраняется). Defaults to None.

    Returns:
        joined_sd_file (list): Объединенный SD файл
    """
    dirname = os.path.dirname(path_to_dir)
    files = os.listdir(dirname)
    
    joined_sd_file = []
    for file in files:
        path_to_file = os.path.join(dirname, file)
        temp_sdf = clean_sdf(path_to_file)
        joined_sd_file.extend(temp_sdf)  
        
    if write_in_file:
        with open(write_in_file, "w") as file:
            for line in joined_sd_file:
                file.write(line)
        if os.path.exists(write_in_file):        
            print("File {} created".format(write_in_file))
        else:
            print("File {} not created".format(write_in_file))
    return joined_sd_file    
