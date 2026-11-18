export interface TeamMember {
  name: string;
  initials: string;
  prn?: string;
  github?: string;
}

/** Project team, in the order shown everywhere in the app and report. */
export const TEAM: TeamMember[] = [
  { name: 'Swamini Mote', initials: 'SM', prn: '202402040005', github: 'swamini9403' },
  { name: 'Neha Shinde', initials: 'NS' },
  { name: 'Vaishnavi Phad', initials: 'VP' },
];

export const APP_NAME = 'LearnSphere';
export const REPO_URL = 'https://github.com/Swamini9403/swamini-lms';
