import ast
import argparse


class AntiPlagiarism:
    def get_ast(self, filename):
        with open(filename, "r") as f:
            s = f.read()
        code = ast.parse(s)
        return ast.dump(code)

    def lev(self, str1, str2):
        n, m = len(str1), len(str2)
        if n > m:
            str1, str2 = str2, str1
            n, m = m, n
        curr = range(n + 1)
        for i in range(1, m + 1):
            prev, curr = curr, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, ch = prev[j] + 1, curr[j - 1] + 1, prev[j - 1]
                if str1[j - 1] != str2[i - 1]:
                    ch += 1
                curr[j] = min(add, delete, ch)

        return curr[n]

    def compare(self, f1, f2):
        code1 = self.get_ast(f1)
        code2 = self.get_ast(f2)
        dist = self.lev(code1, code2)
        length = max(len(code1), len(code2))
        metric = 1 - dist / length
        return metric


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='исходный файл ')
    parser.add_argument('--plagiarism_file', type=str, help='файл, который необходимо проверить на плагиат')

    args = parser.parse_args()
    a = AntiPlagiarism()
    print(a.compare(args.file, args.plagiarism_file))
