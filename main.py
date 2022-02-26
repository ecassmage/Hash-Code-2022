class Contributor:
    def __init__(self, name):
        self.name = name
        self.languages = []
        self.skillLevel = []

    def addLanguage(self, language):
        self.languages.append(language)

    def addSkill(self, skill):
        self.skillLevel.append(int(skill))


class Project:
    def __init__(self, name, lengthOfProject, rewardForCompletion, bestBefore):
        self.name = name
        self.lengthOfProject = lengthOfProject
        self.rewardForCompletion = rewardForCompletion
        self.bestBefore = bestBefore
        self.languages = []
        self.skillLevel = []
        self.assignedContributors = {}

    def addLanguage(self, language):
        self.languages.append(language)
        self.assignedContributors.update({language: None})

    def addSkill(self, skill):
        self.skillLevel.append(int(skill))

    def assignContributor(self, language, contributor):
        for key in self.assignedContributors:
            if self.assignedContributors[key] == contributor:
                return False

        if self.assignedContributors[language] is None:
            self.assignedContributors.update({language: contributor})
            contributor.skillLevel[contributor.languages.index(language)] += 1
            return True
        return False


def parser(inputFile):
    line1, info = [], ""
    counter = 0
    contributors = []
    projects = []
    ObjectPtr = None
    for num, line in enumerate(open("inp\\" + inputFile)):
        line = line.replace("\n", '')
        if num == 0:
            line1 = line.split()
            info = line.split()[1]
            line1 = [int(line1[0]), int(line1[1])]
        elif line1[0] > 0:
            temp = line.split()
            if counter == 0:
                counter = int(temp[1])
                ObjectPtr = Contributor(temp[0])
            else:
                counter -= 1
                ObjectPtr.addLanguage(temp[0])
                ObjectPtr.addSkill(temp[1])

            if counter == 0:
                line1[0] -= 1
                contributors.append(ObjectPtr)

        elif line1[1] > 0:
            temp = line.split()
            if counter == 0:
                counter = int(temp[4])
                ObjectPtr = Project(temp[0], int(temp[1]), int(temp[2]), int(temp[3]))
            else:
                counter -= 1
                ObjectPtr.addLanguage(temp[0])
                ObjectPtr.addSkill(temp[1])

            if counter == 0:
                line1[0] -= 1
                projects.append(ObjectPtr)
    return contributors, projects, info


def logic(contrib: list, proj: list, prevListSize=0):
    if len(proj) == 0:
        return
    failedProjects = []
    successfulProjects = []

    for project in proj:
        for contributor in contrib:
            for language in contributor.languages:
                # temp = best.get(language, contributor)
                # if contributor.skillLevel[contributor.languages.index(language)] >= temp.skillLevel[temp.languages.index(language)]:
                #     temp = contributor
                # best[language] = temp
                if language in project.assignedContributors and contributor.skillLevel[contributor.languages.index(language)] >= project.skillLevel[project.languages.index(language)]:
                    if project.assignContributor(language, contributor):
                        break

        for language in project.languages:
            if project.assignedContributors.get(language, "NotHere, Sorry") is None:
                failedProjects.append(project)
                break
        else:
            successfulProjects.append(project)
    if prevListSize != len(failedProjects) != 0:
        temp = logic(contrib, failedProjects, len(proj))
        for temporary in temp:
            successfulProjects.append(temporary)
    return successfulProjects


def writeOutputs(fileName: str, info: str, projects: list):
    string = info + "\n"

    for project in projects:
        projectString = project.name + "\n"
        for num, key in enumerate(project.assignedContributors):

            if num > 0:
                projectString += " "
            projectString += project.assignedContributors[key].name

        string += projectString + "\n"
    file = open("out\\" + fileName, "w")
    file.write(string)
    file.close()


def idkCheatCleanSomething(projects):
    numberOfValidProjects = 0
    for projectPos in reversed(range(len(projects))):
        for key in projects[projectPos].assignedContributors:
            if projects[projectPos].assignedContributors[key] is None:
                projects.pop(projectPos)
                break
        else:
            numberOfValidProjects += 1
    return projects, numberOfValidProjects


def main():
    array = ['a', 'b', 'c', 'd', 'e', 'f']
    for letter in array:
        contributors, projects, info = parser(f"{letter}.txt")
        projects = logic(contributors, projects)

        writeOutputs(str(letter) + ".txt", info, projects)
        print(f"letter {letter} is Done")
    pass


if __name__ == "__main__":
    main()
