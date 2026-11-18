export interface TeamMember {
  name: string;
  initials: string;
  prn?: string;
  github?: string;
}

/** Project team, in the order shown everywhere in the app and report. */
export const TEAM: TeamMember[] = [
  { name: 'Swamini Mote', initials: 'SM', prn: '202402040005', github: 'swamini9403' },
  { name: 'Neha Shinde', initials: 'NS', prn: '202402040011' },
  { name: 'Vaishnavi Phad', initials: 'VP', prn: '202402040006' },
];

export const APP_NAME = 'LearnSphere';
export const REPO_URL = 'https://github.com/Swamini9403/swamini-lms';
