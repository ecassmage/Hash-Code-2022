class Contributor:
    def __init__(self, name):
        self.name = name
        self.languagesDict = {}

    def addSkill(self, language, skill):
        self.languagesDict.update({self.languages[-1]: int(skill)})


class Project:
    def __init__(self, name, lengthOfProject, rewardForCompletion, bestBefore):
        self.name = name
        self.lengthOfProject = lengthOfProject
        self.rewardForCompletion = rewardForCompletion
        self.bestBefore = bestBefore
        self.languages = []
        self.skillLevel = []
        self.assignedContributors = {}  # {posOrd: {language: contributor}}

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
                ObjectPtr.addSkill(temp[0], temp[1])

            if counter == 0:
                line1[0] -= 1
                contributors.append(ObjectPtr)

        elif line1[1] > 0:
            temp = line.split()
            if temp[0] == 'CollectionsNextv1':
                print(temp[0])
                pass
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
    byLanguage = {}
    for contributor in contributors:
        for language in contributor.languages:
            nextLanguage = byLanguage.get(language, [])
            nextLanguage.append(contributor)
            byLanguage[language] = nextLanguage

    return contributors, byLanguage, projects, info


def choosingLanguage(project: Project, contributorsSorted: dict, contributorsUnsorted: list):
    # languageBuffs = {}
    workingAlready = []
    if project.name == 'CollectionsNextv1':
        print(project.name)
        pass
    for language in project.languages:
        if project.assignedContributors[language] is not None:
            continue
        for contributor in contributorsSorted[language]:
            if contributor in workingAlready:
                continue
            # languageBuffs[language] = languageBuffs.get(language, 0)
            if contributor.languagesDict.get(language, 0) >= project.skillLevel[project.languages.index(language)]:
                project.assignedContributors[language] = contributor
                workingAlready.append(contributor)
                # for ContribLanguage in contributor.languages:
                #     languageBuffs[ContribLanguage] = 1
                break
        else:
            breakout = False
            for contributor in contributorsUnsorted:
                contributorSkill = contributor.languagesDict.get(language, 0)
                if contributorSkill + 1 >= project.skillLevel[project.languages.index(language)]:
                    contribGoodEnough = contributor
                    for languageInnerLoop in project.languages:
                        if languageInnerLoop == language:
                            continue
                        for contributorInnerLoop in contributorsUnsorted:
                            if contributorInnerLoop == contribGoodEnough:
                                continue
                            contributorSkill = contributor.languagesDict.get(languageInnerLoop, 0)
                            if contributorSkill >= project.skillLevel[project.languages.index(language)]:
                                project.assignedContributors[languageInnerLoop] = contributorInnerLoop
                                project.assignedContributors[language] = contribGoodEnough
                                breakout = True
                                break
                    if breakout:
                        break
                if breakout:
                    break

    pass


def logic(people, peopleUnsorted, projects, prevLength=0):
    failed = []
    successful = []

    for project in projects:
        choosingLanguage(project, people, peopleUnsorted)
        for language in project.assignedContributors:
            if project.assignedContributors.get(language, "NotHere, Sorry") is None:
                failed.append(project)
                break
        else:
            successful.append(project)
            for key in project.assignedContributors:
                project.assignedContributors[key].languagesDict[key] = project.assignedContributors[key].languagesDict.get(key, 0) + 1

    if prevLength != len(failed) != 0:
        for project in logic(people, peopleUnsorted, failed, len(projects)):
            successful.append(project)
    return successful


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
            if projects[projectPos].assignedContributors[key] is None or len(projects[projectPos].languages) != len(projects[projectPos].assignedContributors):
                projects.pop(projectPos)
                break
        else:
            numberOfValidProjects += 1
    return projects, numberOfValidProjects


def main():
    for letter in ['a', 'b', 'c', 'd', 'e', 'f']:
        contributors, sortedContributors, projects, info = parser(f"{letter}.txt")
        temp = logic(sortedContributors, contributors, projects)
        tempBetter, info = idkCheatCleanSomething(temp)
        writeOutputs(f"{letter}.txt", str(info), tempBetter)
        print(f"letter {letter} is Done")
    pass


if __name__ == "__main__":
    main()
