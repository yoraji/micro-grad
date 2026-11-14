#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 100
#define NAME_LEN 50

typedef struct {
    char id[15];
    char name[NAME_LEN];
    float scores[3];
    float average;
} Student;

Student students[MAX_STUDENTS];
int count = 0;

void addStudent() {
    if (count >= MAX_STUDENTS) {
        printf("Student list is full!\n");
        return;
    }
    Student s;
    printf("Enter ID: ");
    scanf("%s", s.id);
    printf("Enter name: ");
    scanf("%s", s.name);
    printf("Enter 3 scores: ");
    scanf("%f %f %f", &s.scores[0], &s.scores[1], &s.scores[2]);
    s.average = (s.scores[0] + s.scores[1] + s.scores[2]) / 3.0f;
    students[count++] = s;
    printf("Added successfully.\n");
}

void showAll() {
    if (count == 0) {
        printf("No records.\n");
        return;
    }
    printf("\n%-12s %-15s %8s %8s %8s %8s\n",
           "ID", "Name", "S1", "S2", "S3", "Avg");
    for (int i = 0; i < count; i++) {
        Student s = students[i];
        printf("%-12s %-15s %8.1f %8.1f %8.1f %8.2f\n",
               s.id, s.name, s.scores[0], s.scores[1], s.scores[2], s.average);
    }
}

void searchById() {
    char id[15];
    printf("Enter ID to search: ");
    scanf("%s", id);
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            printf("Found: %s, Avg = %.2f\n",
                   students[i].name, students[i].average);
            return;
        }
    }
    printf("Not found.\n");
}

void saveToFile() {
    FILE *fp = fopen("students.dat", "w");
    if (!fp) { printf("Cannot open file.\n"); return; }
    fprintf(fp, "%d\n", count);
    for (int i = 0; i < count; i++) {
        Student s = students[i];
        fprintf(fp, "%s %s %.2f %.2f %.2f %.2f\n",
                s.id, s.name, s.scores[0], s.scores[1], s.scores[2], s.average);
    }
    fclose(fp);
    printf("Saved to students.dat\n");
}

void loadFromFile() {
    FILE *fp = fopen("students.dat", "r");
    if (!fp) { printf("No saved file.\n"); return; }
    fscanf(fp, "%d", &count);
    for (int i = 0; i < count; i++) {
        Student s;
        fscanf(fp, "%s %s %f %f %f %f",
               s.id, s.name, &s.scores[0], &s.scores[1], &s.scores[2], &s.average);
        students[i] = s;
    }
    fclose(fp);
    printf("Loaded %d records.\n", count);
}

int main() {
    int choice;
    do {
        printf("\n=== Grade Manager ===\n");
        printf("1. Add  2. Show All  3. Search\n");
        printf("4. Save  5. Load  6. Exit\n");
        printf("Choose: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: addStudent(); break;
            case 2: showAll();    break;
            case 3: searchById(); break;
            case 4: saveToFile(); break;
            case 5: loadFromFile(); break;
            case 6: printf("Bye!\n"); break;
            default: printf("Invalid choice.\n");
        }
    } while (choice != 6);

    return 0;
}