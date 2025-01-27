---
Author:
  - Ширяев Антон
tags:
  - Singularity
date: 2025-01-21
---
# О Singularity

Singularity (сейчас известный как **Apptainer**) — это популярный инструмент для работы с контейнерами, который особенно востребован в высокопроизводительных вычислениях (HPC) и научных исследованиях. В отличие от Docker, Singularity разработан с учетом специфики HPC-кластеров, где важны безопасность, воспроизводимость и интеграция с системами управления задачами, такими как Slurm.

---

### Основные особенности Singularity/Apptainer

1. **Безопасность**:
   - Singularity позволяет пользователям запускать контейнеры без прав суперпользователя (root). Это критически важно для многопользовательских HPC-кластеров, где пользователи не имеют административных прав.
   - Контейнеры изолированы, но интегрированы с системой, что позволяет использовать ресурсы кластера (например, GPU) и работать с файловой системой.

2. **Поддержка Docker**:
   - Singularity может напрямую работать с Docker-образами, скачивая их из Docker Hub и конвертируя в собственный формат.
   - Пример: `singularity pull docker://ubuntu:latest` скачает образ Ubuntu из Docker Hub и создаст файл `ubuntu_latest.sif`.

3. **Портативность**:
   - Контейнеры Singularity сохраняются в виде единого файла (обычно с расширением `.sif`), который можно легко переносить между системами.
   - Это упрощает воспроизводимость исследований: вы можете создать контейнер с нужным ПО и передать его коллегам или использовать на другом кластере.

4. **Интеграция с HPC**:
   - Singularity отлично работает с системами управления задачами, такими как Slurm.
   - Контейнеры могут использовать ресурсы кластера (например, MPI для параллельных вычислений) и работать с распределенными файловыми системами (NFS, Lustre, GPFS).

5. **Поддержка GPU**:
   - Singularity поддерживает GPU через интеграцию с CUDA и другими фреймворками, что делает его идеальным для задач машинного обучения и научных вычислений.

---

### Основные команды Singularity

1. **Скачивание Docker-образа**:
   ```bash
   singularity pull docker://ubuntu:latest
   ```
   Скачивает образ Ubuntu из Docker Hub и сохраняет его в формате `.sif`.

2. **Запуск контейнера**:
   ```bash
   singularity run ubuntu_latest.sif
   ```
   Запускает контейнер и выполняет его стандартную команду (обычно это командная оболочка или приложение).

3. **Интерактивный запуск**:
   ```bash
   singularity shell ubuntu_latest.sif
   ```
   Открывает интерактивную командную оболочку внутри контейнера.

4. **Выполнение команды в контейнере**:
   ```bash
   singularity exec ubuntu_latest.sif ls /
   ```
   Выполняет команду `ls /` внутри контейнера.

5. **Сборка контейнера из определения**:
   Singularity позволяет создавать контейнеры из файла определения (`.def`). Пример файла `my_container.def`:
   ```bash
   Bootstrap: docker
   From: ubuntu:latest

   %post
       apt-get update && apt-get install -y python3
   ```
   Сборка контейнера:
   ```bash
   singularity build my_container.sif my_container.def
   ```

6. **Монтирование директорий**:
   - По умолчанию Singularity монтирует домашнюю директорию пользователя и текущую рабочую директорию.
   - Вы можете указать дополнительные директории для монтирования с помощью опции `--bind`:
     ```bash
     singularity run --bind /path/on/host:/path/in/container my_container.sif
     ```

---

### Пример использования Singularity с Slurm

1. **Создание скрипта для Slurm**:
   ```bash
   #!/bin/bash
   #SBATCH --job-name=singularity_example
   #SBATCH --output=output.txt
   #SBATCH --error=error.txt
   #SBATCH --ntasks=1
   #SBATCH --time=00:10:00
   #SBATCH --partition=your_partition_name

   # Запуск контейнера
   singularity exec my_container.sif python3 my_script.py
   ```

2. **Отправка задачи**:
   ```bash
   sbatch my_slurm_script.sh
   ```

---

### Преимущества Singularity перед Docker в HPC

1. **Безопасность**:
   - Docker требует прав root для работы, что не подходит для многопользовательских кластеров.
   - Singularity запускается от имени пользователя, что делает его безопасным для использования на HPC.

2. **Интеграция с HPC**:
   - Singularity поддерживает MPI, GPU и другие технологии, используемые в HPC.
   - Docker не всегда хорошо интегрируется с системами управления задачами, такими как Slurm.

3. **Портативность**:
   - Singularity создает один файл (`.sif`), который легко переносить между системами.
   - Docker требует наличия Docker Engine и репозитория для хранения образов.

---

### Недостатки Singularity

1. **Меньше сообщество**:
   - Сообщество Singularity меньше, чем у Docker, поэтому документация и поддержка могут быть менее доступны.

2. **Ограниченная функциональность**:
   - Singularity не поддерживает все функции Docker, такие как Docker Compose или Docker Swarm.

3. **Сложность сборки**:
   - Сборка контейнеров в Singularity может быть сложнее, особенно для пользователей, привыкших к Docker.

---

### Singularity vs Apptainer

- **Singularity** был оригинальным проектом, разработанным в Lawrence Berkeley National Laboratory.
- В 2021 году проект был переименован в **Apptainer** и стал частью Linux Foundation. Это было сделано для обеспечения более открытого и устойчивого развития.
- Apptainer сохраняет обратную совместимость с Singularity, поэтому большинство команд и функций остаются теми же.

---

### Полезные ресурсы

1. **Официальная документация**:
   - [Apptainer Documentation](https://apptainer.org/docs/)
   - [Singularity Documentation](https://sylabs.io/guides/3.0/user-guide/)

2. **Репозиторий на GitHub**:
   - [Apptainer](https://github.com/apptainer/apptainer)
   - [Singularity](https://github.com/sylabs/singularity)

3. **Примеры использования**:
   - [Singularity Recipes](https://github.com/sylabs/singularity-examples)


