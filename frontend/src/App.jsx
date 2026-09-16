import { useState } from 'react';
import { ArrowDown, ArrowUpRight, BrainCircuit, ChevronRight, Cpu, Globe, Mail, Menu, Network, Phone, X } from 'lucide-react';
import ChatWidget from './components/ChatWidget.jsx';

const projects = [
  ['01', 'Car Price Prediction', 'Regression modeling', 'Cleaned, analyzed, and modeled used-car data to predict second-hand prices.', 'ai-card ai-card-sand'],
  ['02', "Alzheimer's Prediction", 'Healthcare AI', 'Used exploratory analysis and regression techniques to support early disease prediction.', 'ai-card ai-card-night'],
  ['03', 'Attendance Tracker', 'Computer vision system', 'Improved recognition accuracy by 95% and cut manual tracking time by 80%.', 'ai-card ai-card-dark'],
  ['04', 'Corn Disease AI', 'Agritech diagnostics', 'A leaf-image model for identifying disease symptoms with over 90% accuracy.', 'ai-card ai-card-green'],
  ['05', 'Dog Breed Classifier', 'Image classification', 'A model that identifies 70 dog breeds and returns breed-level information.', 'ai-card ai-card-purple'],
  ['06', 'Vehicle Tracking', 'YOLO object detection', 'Real-time vehicle detection with structured tracking data storage.', 'ai-card ai-card-blue'],
  ['07', 'Image to Text', 'AI extraction pipeline', 'Camera-captured text converted into structured CSV data.', 'ai-card ai-card-sand'],
  ['08', 'Plant Disease AI', 'Leaf analysis', 'Early-stage plant disease prediction through detailed leaf-image analysis.', 'ai-card ai-card-green'],
  ['09', 'Brain Tumour Detection', 'Medical imaging', 'Deep learning classification for brain tumour analysis and insights.', 'ai-card ai-card-night'],
  ['10', 'Monkey Pox Detection', 'Healthcare AI', 'Early-stage disease detection and analysis from medical image data.', 'ai-card ai-card-purple'],
  ['11', 'Company Tracker', 'Live camera system', 'Employee registration and automated attendance using a live camera feed.', 'ai-card ai-card-blue'],
];

const experience = [
  ['01', 'Assistant Manager', 'Learning Links Foundation / Dell Technologies', '2023 — Present', 'Productivity +20% · delivery time -15% · onboarding time -30% · savings 10%'],
  ['02', 'Robotic Trainer', 'Wunderkastan Robotian Education Pvt Ltd', '2022 — 2023', 'Arduino · embedded systems · robotics curriculum · workshops'],
  ['03', 'MI Engineer', 'White Vectors', '2020 — 2021', 'Predictive models · data preparation · visual analytics · forecasting'],
  ['04', 'Hardware Testing Engineer', 'Transsion Holding Pvt Ltd', '2018 — 2020', 'SMT testing · mobile hardware QA · defect analysis'],
];

const education = [
  ['B.E./B.Tech', 'Electronics and Communications Engineering', 'Anna University Chennai · 2013'],
  ['Intermediate', 'Physics, Chemistry and Mathematics', 'Patna Science College · 2007'],
  ['10th', 'Secondary education', 'D.A.V Public School, Rajrappa · 2005'],
];

const certifications = [
  'Data Science Certification Course · Social Prachar Hyderabad',
  'Online Certificate Program in Artificial Intelligence and Machine Learning · EXCELR',
];

const skillGroups = [
  ['01', 'MODELING', 'Building prediction systems from experiments to useful outcomes.', BrainCircuit, ['Machine Learning', 'Deep Learning', 'Regression', 'Classification', 'Predictive Modeling']],
  ['02', 'DATA SYSTEMS', 'Cleaning, structuring, and connecting data to decisions.', Network, ['Python', 'Pandas', 'NumPy', 'SQL', 'ChromaDB', 'Feature Engineering']],
  ['03', 'INTELLIGENCE', 'Exploring language, images, and generative systems.', Globe, ['NLP', 'Generative AI', 'LLMs', 'YOLO', 'Computer Vision']],
  ['04', 'HARDWARE', 'Making intelligence tangible through circuits and robots.', Cpu, ['Robotics', 'Arduino', 'Embedded Systems', 'Circuit Testing', 'SMT QA']],
];

function Nav({ open, setOpen }) {
  const links = ['about', 'skills', 'experience', 'projects', 'contact'];
  return <header className="reference-nav"><a href="#home" className="reference-brand">SANJEEV KUMAR</a><button className="mobile-menu" onClick={() => setOpen(!open)} aria-label="Open menu">{open ? <X size={21} /> : <Menu size={21} />}</button><nav className={open ? 'open' : ''}>{links.map((link) => <a href={`#${link}`} key={link} onClick={() => setOpen(false)}>{link.toUpperCase()}</a>)}</nav></header>;
}

function PageTitle({ title, number }) {
  return <div className="page-title"><span>{number}</span><h2>{title}</h2></div>;
}

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const moveHero = (event) => {
    const bounds = event.currentTarget.getBoundingClientRect();
    const x = ((event.clientX - bounds.left) / bounds.width - 0.5) * 2;
    const y = ((event.clientY - bounds.top) / bounds.height - 0.5) * 2;
    event.currentTarget.style.setProperty('--hero-x', `${x}`);
    event.currentTarget.style.setProperty('--hero-y', `${y}`);
  };

  return <div className="reference-site">
    <div className="reference-grid" aria-hidden="true" />
    <Nav open={menuOpen} setOpen={setMenuOpen} />

    <main>
      <section id="home" className="home-page page-panel" onPointerMove={moveHero}>
        <div className="hero-orbit orbit-one" /><div className="hero-orbit orbit-two" />
        <h1 className="hero-title">HI, I'M <span>SANJEEV</span></h1>
        <div className="hero-portrait"><img src="/avatar.jpg" alt="Illustrated portrait of Sanjeev Kumar" /></div>
        <p className="hero-description">A DATA SCIENTIST EXPERIENCED IN<br />BUILDING USEFUL INTELLIGENCE.</p>
        <a href="#contact" className="hero-contact">CONTACT ME <ArrowUpRight size={19} /></a>
        <a className="scroll-cue" href="#about"><ArrowDown size={18} /> SCROLL TO EXPLORE</a>
      </section>

      <section className="work-reel" aria-label="Selected work reel"><div className="reel-track">{projects.concat(projects).map(([number, title, category, description, color], index) => <article className={color} key={`${title}-${index}`}><span>{category}</span><strong>{title}</strong><small>{description}</small><i>{number}</i></article>)}</div></section>

      <section id="about" className="about-page page-panel"><PageTitle number="01" title="ABOUT ME" /><div className="about-object object-left">✦</div><div className="about-object object-right">◈</div><div className="about-content"><p className="about-statement">A BUILDER WHO LIKES<br /><em>USEFUL INTELLIGENCE.</em></p><p>Results-driven Data Scientist and ML Engineer with a strong foundation in artificial intelligence, machine learning, and data analysis. I enjoy transforming ambiguous problems into clean experiments and systems people can actually use.</p><p>My work crosses predictive modeling, computer vision, generative AI, robotics, and educational technology.</p></div><div className="side-label">SANJEEV KUMAR / 2026</div></section>

      <section id="skills" className="skills-page page-panel white-page"><PageTitle number="02" title="SKILLS" /><div className="skill-scanner"><span>SKILL PROFICIENCY SCANNER</span><strong>APPLIED AI / ML</strong><div className="scanner-line"><i /></div><b>ACTIVE</b></div><div className="skill-grid">{skillGroups.map(([number, title, description, Icon, skills]) => <article className="skill-card" key={title}><div className="skill-card-top"><span> CATEGORY {number}</span><Icon size={24} /></div><h3>{title}</h3><p>{description}</p><div className="skill-pills">{skills.map((skill) => <span key={skill}>{skill}</span>)}</div></article>)}</div></section>

      <section id="experience" className="experience-page page-panel"><PageTitle number="03" title="EXPERIENCE" /><div className="experience-intro"><p>FOUR ROLES.<br /><em>ONE CONTINUOUS BUILD.</em></p><span>From hardware quality to applied machine learning, every role has sharpened the way I solve problems.</span></div><div className="experience-table">{experience.map(([number, role, company, date, result]) => <article key={company}><span className="experience-number">{number}</span><div><h3>{role}</h3><p className="experience-company">{company}</p></div><span className="experience-date">{date}</span><p className="experience-result">{result}</p><ChevronRight size={22} /></article>)}</div></section>

      <section id="projects" className="projects-page page-panel"><PageTitle number="04" title="PROJECTS" /><div className="project-intro"><p>SELECTED AI SYSTEMS<br /><em>FROM THE LAB.</em></p><span>11 projects across computer vision, healthcare, agritech, NLP, and predictive analytics.</span></div><div className="project-gallery">{projects.map(([number, title, category, description, color]) => <article className={color} key={title}><div className="project-card-number">{number}<ArrowUpRight size={18} /></div><div className="project-art"><span>{category}</span><strong>{title}</strong><div className="art-lines" /></div><p>{description}</p><a href="#contact">VIEW CASE <ArrowUpRight size={15} /></a></article>)}</div><div className="credentials-strip"><div><span>EDUCATION</span>{education.map(([degree, subject, details]) => <p key={degree}><strong>{degree}</strong> {subject}<small>{details}</small></p>)}</div><div><span>CERTIFICATIONS</span>{certifications.map((certification) => <p key={certification}>{certification}</p>)}</div></div></section>

      <section id="contact" className="contact-page page-panel white-page"><PageTitle number="05" title="CONTACT" /><div className="contact-content"><p>LET'S BUILD<br /><em>SOMETHING USEFUL.</em></p><div className="terminal-form"><div><span>contact.init()</span><b>● ● ●</b></div><label>YOUR NAME<input placeholder="sanjeev@your-company" /></label><label>YOUR MESSAGE<textarea placeholder="Tell me about the problem worth solving..." rows="3" /></label><div className="terminal-actions"><button type="button">CLEAR</button><button type="button">SEND <ArrowUpRight size={15} /></button></div></div><a className="contact-big-link" href="mailto:sanjeevr26@gmail.com">sanjeevr26@gmail.com <ArrowUpRight size={24} /></a><div className="contact-details"><span>HYDERABAD, INDIA</span><span>AVAILABLE FOR AI / ML WORK</span><div><a href="https://www.linkedin.com/in/sanjeev-kumar-0398bb35" target="_blank" rel="noreferrer"><Globe size={19} /></a><a href="mailto:sanjeevr26@gmail.com"><Mail size={19} /></a><a href="tel:+918860223417"><Phone size={19} /></a></div></div></div><footer>© 2026 SANJEEV KUMAR <span>BUILT WITH CURIOSITY</span></footer></section>
    </main>
    <ChatWidget />
  </div>;
}
