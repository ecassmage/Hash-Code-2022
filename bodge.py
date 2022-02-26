class Contributor:
    def __init__(self, name):
        self.name = name
        self.languages = {}

    def addSkill(self, language, skill):
        self.languages.update({language: int(skill)})


class Project:
    def __init__(self, name, lengthOfProject, rewardForCompletion, bestBefore):
        self.name = name
        self.lengthOfProject = lengthOfProject
        self.rewardForCompletion = rewardForCompletion
        self.bestBefore = bestBefore
        self.languages = []
        self.skillLevel = []
        self.contributors = []

    def addLanguage(self, language):
        self.languages.append(language)
        self.contributors.append(None)

    def addSkill(self, skill):
        self.skillLevel.append(int(skill))

    def assignContributor(self, language, contributor):
        for key in range(len(self.languages)):
            if self.contributors[key] == contributor:
                return False

        if self.contributors[self.languages.index(language)] is None:
            self.contributors.append(contributor)
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


def findMentor(people, project, language):
    for person in people[language]:
        for num, languageInProj in enumerate(project.languages):
            if language == languageInProj:
                continue
            if person.languages.get(language, 0) >= project.skillLevel[project.languages.index(language)]:
                if person not in project.contributors:
                    project.contributors[num] = person
                    return True
    return False


def findNewbie(people, project, language):
    for languageOfPeople in people:
        for person in people[languageOfPeople]:
            if person.languages.get(language, 0) + 1 >= project.skillLevel[project.languages.index(language)]:
                if findMentor(people, project, language):
                    project.contributors[project.languages.index(language)] = person
                return


def checkForFail(people, project, loop=True):
    for num, contributor in enumerate(project.contributors):
        if contributor is None:
            if loop:
                findNewbie(people, project, project.languages[num])
                return checkForFail(people, project, False)
            return True
    return False


def logic(people, projects, prevLength=0):
    successful = []
    failed = []
    for project in projects:
        for num, language in enumerate(project.languages):
            for contributor in people[language]:
                if project.contributors[num] is None and contributor.languages[language] >= project.skillLevel[num] and contributor not in project.contributors:
                    project.contributors[num] = contributor
                    break
        if checkForFail(people, project):
            failed.append(project)
        else:
            for num, contributor in enumerate(project.contributors):
                if contributor.languages.get(project.languages[num], 0) <= project.skillLevel[num]:
                    contributor.languages[project.languages[num]] = contributor.languages.get(project.languages[num], 0) + 1
            successful.append(project)
    if prevLength != len(failed) != 0:
        for project in logic(people, failed, len(projects)):
            successful.append(project)
    return successful


def writeOutputs(fileName: str, projects: list):
    string = str(len(projects)) + "\n"

    for project in projects:
        projectString = project.name + "\n"
        for num, contributor in enumerate(project.contributors):

            if num > 0:
                projectString += " "
            projectString += contributor.name

        string += projectString + "\n"
    file = open("out\\" + fileName, "w")
    file.write(string)
    file.close()


def main():
    for letter in ['a', 'b', 'c', 'd', 'e', 'f']:
        contributors, sortedContributors, projects, info = parser(f"{letter}.txt")
        temp = logic(sortedContributors, projects)
        writeOutputs(f"{letter}.txt", temp)
        print(f"letter {letter} is Done")
    pass


if __name__ == "__main__":
    main()