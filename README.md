# AUD_Practice-Now
AUD_Practice Now
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AUD Exam Trainer - Topic-Based Study</title>
  <style>
    :root { color-scheme: dark; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
      background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
      color: #e8eaf6;
      min-height: 100vh;
      padding: 20px;
    }
    .container { max-width: 700px; margin: 0 auto; }
    .card {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 30px;
      backdrop-filter: blur(10px);
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
      margin-bottom: 20px;
    }
    h1 {
      font-size: 32px;
      margin-bottom: 10px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .subtitle { color: #b0b3c1; margin-bottom: 30px; font-size: 14px; }
    .topic-grid { display: grid; gap: 12px; margin: 20px 0; }
    .topic-btn {
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
      border: 2px solid rgba(102, 126, 234, 0.3);
      border-radius: 15px;
      padding: 20px;
      color: #e8eaf6;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      text-align: left;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .topic-btn:hover {
      transform: translateY(-2px);
      border-color: rgba(102, 126, 234, 0.6);
      box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    .topic-btn.selected {
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
      border-color: rgba(102, 126, 234, 0.8);
    }
    .badge {
      background: rgba(102, 126, 234, 0.3);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 700;
    }
    button {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      border-radius: 12px;
      padding: 16px 32px;
      color: white;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.3s ease;
      width: 100%;
      margin-top: 10px;
    }
    button:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
    button:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
    button.secondary {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .quiz-screen { display: none; }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 15px;
      margin: 20px 0;
    }
    .stat {
      background: rgba(0, 0, 0, 0.3);
      border-radius: 12px;
      padding: 15px;
      text-align: center;
    }
    .stat-label { color: #b0b3c1; font-size: 12px; margin-bottom: 8px; }
    .stat-value { font-size: 28px; font-weight: 900; }
    .progress-bar {
      height: 8px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      overflow: hidden;
      margin: 20px 0;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
      transition: width 0.4s ease;
    }
    .question {
      background: rgba(0, 0, 0, 0.3);
      border-radius: 15px;
      padding: 25px;
      margin: 20px 0;
      font-size: 18px;
      line-height: 1.6;
      border-left: 4px solid #667eea;
    }
    .choices { display: grid; gap: 12px; margin: 20px 0; }
    .choice {
      background: rgba(255, 255, 255, 0.05);
      border: 2px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 16px;
      cursor: pointer;
      transition: all 0.3s ease;
      font-size: 15px;
    }
    .choice:hover { background: rgba(255, 255, 255, 0.1); border-color: rgba(102, 126, 234, 0.5); }
    .choice.correct {
      background: rgba(76, 175, 80, 0.2);
      border-color: #4CAF50;
      animation: pulse 0.5s ease;
    }
    .choice.wrong {
      background: rgba(244, 67, 54, 0.2);
      border-color: #F44336;
      animation: shake 0.5s ease;
    }
    .choice.disabled { cursor: not-allowed; opacity: 0.6; }
    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.02); }
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-5px); }
      75% { transform: translateX(5px); }
    }
    .rationale {
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
      border: 1px solid rgba(102, 126, 234, 0.3);
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
      display: none;
      line-height: 1.6;
    }
    .btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
    .pill {
      display: inline-block;
      background: rgba(102, 126, 234, 0.2);
      border: 1px solid rgba(102, 126, 234, 0.4);
      border-radius: 20px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      margin: 5px;
    }
    .slider-container { margin: 20px 0; }
    .slider-label { margin-bottom: 10px; font-weight: 600; }
    input[type="range"] {
      width: 100%;
      height: 8px;
      border-radius: 5px;
      background: rgba(255, 255, 255, 0.1);
      outline: none;
      -webkit-appearance: none;
    }
    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #667eea;
      cursor: pointer;
    }
    .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <div id="homeScreen">
      <div class="card">
        <h1>🎯 AUD Exam Trainer</h1>
        <div class="subtitle">Comprehensive practice for all major AUD topics • Track your progress</div>
        
        <h2 style="margin: 30px 0 15px; font-size: 20px;">Select a Topic</h2>
        <div class="topic-grid" id="topicGrid"></div>
        
        <div class="slider-container">
          <div class="slider-label">Quiz Size: <span id="sizeLabel">25</span> questions</div>
          <input type="range" id="sizeSlider" min="10" max="50" value="25" step="5">
        </div>
        
        <button id="startBtn" disabled>Select a topic to begin</button>
        <button class="secondary" id="resetBtn">Reset All Progress</button>
      </div>
    </div>
    
    <div id="quizScreen" class="quiz-screen">
      <div class="card">
        <div class="header-row">
          <span class="pill" id="topicLabel">Topic</span>
          <span class="pill" id="progressLabel">1/25</span>
        </div>
        
        <div class="progress-bar">
          <div class="progress-fill" id="progressBar" style="width: 0%"></div>
        </div>
        
        <div class="stats">
          <div class="stat">
            <div class="stat-label">CORRECT</div>
            <div class="stat-value" style="color: #4CAF50;" id="correctStat">0</div>
          </div>
          <div class="stat">
            <div class="stat-label">WRONG</div>
            <div class="stat-value" style="color: #F44336;" id="wrongStat">0</div>
          </div>
          <div class="stat">
            <div class="stat-label">SCORE</div>
            <div class="stat-value" style="color: #667eea;" id="scoreStat">0%</div>
          </div>
        </div>
        
        <div class="question" id="questionText"></div>
        
        <div class="choices" id="choicesDiv"></div>
        
        <div class="rationale" id="rationaleDiv"></div>
        
        <div class="btn-group">
          <button id="showBtn">Show Answer</button>
          <button id="nextBtn">Next →</button>
        </div>
        
        <button class="secondary" id="exitBtn" style="margin-top: 10px;">Exit to Topics</button>
      </div>
    </div>
  </div>

  <script>
    // Question bank
    const TOPICS = {
      ethics: {
        name: "Ethics & Independence",
        questions: [
          {q: "Which independence threat exists when an auditor audits their own firm's prior work?", c: ["Self-review threat", "Advocacy threat", "Familiarity threat", "Management participation threat"], a: 0, r: "Self-review threat occurs when auditing work you previously performed."},
          {q: "Under AICPA rules, can an auditor perform bookkeeping for an audit client?", c: ["Yes, if client assumes all management responsibilities", "No, never permitted", "Yes, with no restrictions", "Only for non-SEC clients"], a: 0, r: "Bookkeeping is permitted if the client assumes management responsibility."},
          {q: "Professional skepticism is best described as:", c: ["A questioning mind and critical assessment of evidence", "Assuming management is dishonest", "Accepting management representations", "Only when fraud suspected"], a: 0, r: "Professional skepticism requires a questioning mindset throughout."},
          {q: "Which scenario creates an advocacy threat?", c: ["Promoting client's securities to investors", "Long relationship with management", "Auditing prior work", "Client fee pressure"], a: 0, r: "Advocacy threat arises when promoting the client's position."},
          {q: "When can a CPA disclose confidential client information?", c: ["Valid subpoena or regulatory inquiry", "Friend for advice", "Social media case study", "Fee negotiations"], a: 0, r: "Confidentiality has exceptions for legal/regulatory requirements."},
          {q: "Independence is impaired if the CPA has:", c: ["Direct financial interest in audit client", "Immaterial indirect interest", "Auto loan from client bank", "Checking account under FDIC limits"], a: 0, r: "Direct financial interests impair independence regardless of materiality."},
          {q: "Which service creates a management participation threat?", c: ["Making management decisions for client", "Providing tax advice", "Preparing financial statements", "Internal audit work"], a: 0, r: "Management participation occurs when making management decisions."},
          {q: "The Code of Professional Conduct applies to:", c: ["All professional services by AICPA members", "Only audit engagements", "Only SEC clients", "Only public companies"], a: 0, r: "The Code applies to all professional services by members."},
          {q: "Which creates a familiarity threat?", c: ["Long-standing close relationship with client", "First-year audit", "Annual team rotation", "Using client documents"], a: 0, r: "Familiarity threats arise from close relationships."},
          {q: "Covered members include:", c: ["Engagement team and those who can influence", "Only engagement partner", "Only employees with client contact", "Only partners"], a: 0, r: "Covered members include team and those able to influence."},
          {q: "Independence rules for non-attest services require:", c: ["Client assumes all management responsibilities", "CPA makes significant decisions", "Services after audit", "Board approval only"], a: 0, r: "Non-attest services require client to assume management responsibility."},
          {q: "Due professional care requires:", c: ["Competence and diligence consistent with engagement", "Guaranteeing accuracy", "Detecting all fraud", "Unlimited time"], a: 0, r: "Due care means applying professional competence and diligence."},
          {q: "A CPA's spouse owns stock in an audit client. Independence is:", c: ["Impaired due to immediate family", "Not impaired if immaterial", "Not impaired if disclosed", "Only impaired for SEC"], a: 0, r: "Immediate family's direct interest impairs independence."},
          {q: "Acceptable safeguard for independence:", c: ["Quality review by uninvolved partner", "Increasing fees", "Extended tenure", "Client approval"], a: 0, r: "Quality reviews serve as effective safeguards."},
          {q: "Integrity requires a CPA to:", c: ["Be honest within professional constraints", "Disclose all info publicly", "Never disagree with management", "Accept all clients"], a: 0, r: "Integrity means being straightforward while respecting confidentiality."},
          {q: "When are contingent fees prohibited?", c: ["For any attest engagement", "All professional services", "Only SEC clients", "Never prohibited"], a: 0, r: "Contingent fees prohibited for attest services."},
          {q: "Professional competence requires:", c: ["Maintaining knowledge through CPE", "Accepting all engagements", "Past experience only", "No specialization"], a: 0, r: "CPAs must maintain competence through continuing education."},
          {q: "Objectivity is best maintained by:", c: ["Avoiding conflicts of interest", "Maximizing fees", "Long relationships", "Accepting management judgments"], a: 0, r: "Objectivity requires freedom from conflicts."},
          {q: "Acts discreditable include:", c: ["Discrimination and harassment", "Premium fees", "Declining engagements", "Industry specialization"], a: 0, r: "Discriminatory conduct is discreditable to the profession."},
          {q: "Loan from financial institution client that doesn't impair:", c: ["Auto loan under normal terms", "Material loan not normal terms", "Loan secured by audit services", "Unsecured line of credit"], a: 0, r: "Normal lending procedure loans don't impair independence."},
          {q: "Conceptual framework for independence requires:", c: ["Identifying, evaluating, addressing threats", "Following only rules", "Avoiding all services", "Client waivers"], a: 0, r: "Framework requires systematic threat management."},
          {q: "Fee dependency creates:", c: ["Undue influence threat requiring safeguards", "No threat if disclosed", "Automatic impairment", "Non-mitigable self-interest"], a: 0, r: "Fee dependency requires evaluation and safeguards."},
          {q: "Former employment impairs independence if:", c: ["Recent and in key position with influence", "More than 5 years ago", "Non-financial position", "Disclosed in report"], a: 0, r: "Recent employment in key positions creates threats."},
          {q: "Professional behavior means:", c: ["Complying with laws avoiding discreditable acts", "Agreeing with client", "Maximizing profit", "Avoiding controversial clients"], a: 0, r: "Professional behavior requires legal compliance."},
          {q: "CPA preparing tax returns for audit client:", c: ["May do with safeguards", "Impairs automatically", "Requires SEC approval", "Prohibited"], a: 0, r: "Tax services permitted with safeguards for non-SEC."},
          {q: "When must CPA withdraw?", c: ["Independence impaired and cannot be resolved", "Fee disputes", "Extensive procedures", "Management disagrees"], a: 0, r: "Unresolvable independence impairment requires withdrawal."},
          {q: "PCAOB independence rules apply to:", c: ["Auditors of public companies", "All AICPA members", "Only Big 4 firms", "Government auditors"], a: 0, r: "PCAOB rules govern public company auditors."},
          {q: "Relationship that impairs independence:", c: ["Partner's spouse in key client position", "Different office immaterial investment", "Janitorial staff relative", "Admin staff banks at client"], a: 0, r: "Immediate family in key positions impairs independence."},
          {q: "Professional skepticism requires:", c: ["Critical assessment even with honest clients", "Assuming dishonesty", "Accepting management's word", "Only with fraud indicators"], a: 0, r: "Skepticism maintained even with honest clients."},
          {q: "CPA may NOT accept commission for:", c: ["Referring attest client to service provider", "Referring non-attest client", "Selling to non-client", "Educational seminars"], a: 0, r: "Commissions prohibited for attest client referrals."},
          {q: "Undue influence threat created by:", c: ["Client threatens to replace auditor", "Client pays promptly", "Strong controls", "Provides requested info"], a: 0, r: "Pressure from client creates undue influence threats."},
          {q: "GAO independence standards apply to:", c: ["Government financial audits", "Only federal audits", "All AICPA members", "Private sector only"], a: 0, r: "GAO standards govern government financial audits."},
          {q: "May use client confidential info for:", c: ["Authorized quality review", "Business development", "Social media studies", "Training unrelated staff"], a: 0, r: "May use for authorized quality reviews."},
          {q: "Independence in appearance means:", c: ["Reasonable third party would conclude independent", "Auditor believes independent", "Client believes", "No actual conflicts"], a: 0, r: "Appearance requires reasonable third party view."},
          {q: "Network firm relationship:", c: ["May create issues requiring evaluation", "Never affects independence", "Automatically impairs", "Only for SEC clients"], a: 0, r: "Network relationships need assessment."},
          {q: "Subordination of judgment occurs when:", c: ["CPA allows override of professional conclusion", "Consults supervisor", "Follows firm policy", "Uses templates"], a: 0, r: "Subordination means improperly deferring judgment."},
          {q: "Violates confidentiality:", c: ["Social event discussion", "Court testimony", "Ethics inquiry response", "Peer review documents"], a: 0, r: "Casual social disclosure violates confidentiality."},
          {q: "CPA learns tax return has material error:", c: ["Inform client and recommend correction", "Notify IRS immediately", "Withdraw", "Ignore if prior year"], a: 0, r: "Must inform client and advise correction."},
          {q: "Rotating engagement partners:", c: ["Addresses familiarity threats", "Required for all clients", "Impairs independence", "Only SEC clients"], a: 0, r: "Rotation mitigates familiarity threats."},
          {q: "Professional judgment means:", c: ["Applying training, knowledge, experience", "Following management", "Using only templates", "Avoiding decisions"], a: 0, r: "Judgment requires applying competence and experience."},
          {q: "Independence of mind refers to:", c: ["Mental state permitting objective conclusions", "How auditor appears", "Educational background", "Years of experience"], a: 0, r: "Independence of mind is mental state for unbiased judgments."},
          {q: "CPA may serve as client's:", c: ["Transaction advisor with safeguards", "CFO", "Controller making decisions", "Voting board member"], a: 0, r: "Advisory roles permitted; management positions impair."},
          {q: "Former partner joins client. Independence requires:", c: ["Cooling-off and evaluation", "Immediate impairment", "No impact if disclosed", "Only SEC matters"], a: 0, r: "Employment requires cooling-off and assessment."},
          {q: "Principle emphasizing maintaining skills:", c: ["Professional competence and due care", "Integrity", "Objectivity", "Confidentiality"], a: 0, r: "Competence principle requires maintaining skills."},
          {q: "Covered member's close relative includes:", c: ["Parent, sibling, non-dependent child", "Spouse only", "No relatives", "Only dependents"], a: 0, r: "Close relatives include parents, siblings, non-dependent children."},
          {q: "Discovers illegal acts during audit:", c: ["Communicate to governance", "Report to authorities immediately", "Ignore unless material", "Document and take no action"], a: 0, r: "Illegal acts require governance communication."},
          {q: "Hosting arrangement may impair:", c: ["Auditor hosts client financial system", "Client hosts own systems", "Cloud accounting software", "Firm hosts own systems"], a: 0, r: "Hosting client data may create threats."},
          {q: "Professional skepticism applies to:", c: ["All evidence throughout engagement", "Only unusual transactions", "Only when fraud suspected", "Only high-risk areas"], a: 0, r: "Skepticism maintained for all evidence throughout."},
          {q: "Auditor must withdraw when:", c: ["Independence impaired and unresolvable", "Fees disputed", "Procedures extensive", "Management disagrees"], a: 0, r: "Unresolvable independence requires withdrawal."},
          {q: "Acceptable independence safeguard:", c: ["Quality review by independent partner", "Increased fees", "Extended tenure", "Client procedure approval"], a: 0, r: "Independent quality reviews are effective safeguards."}
        ]
      },
      
      evidence: {
        name: "Evidence & Procedures",
        questions: [
          {q: "Which audit evidence is generally most reliable?", c: ["External confirmation from independent third party", "Client-prepared schedule", "Management representation", "Client photocopy"], a: 0, r: "External evidence from independent sources is most reliable."},
          {q: "Sufficient appropriate evidence means:", c: ["Adequate quantity and suitable quality", "Maximum possible procedures", "Client's preferred documentation", "Industry standard minimums"], a: 0, r: "Evidence must satisfy both quantity and quality requirements."},
          {q: "Test of controls evaluates:", c: ["Operating effectiveness of internal controls", "Account balance accuracy", "Transaction dollar amounts", "Detection risk levels"], a: 0, r: "Control tests assess how effectively controls operate."},
          {q: "Substantive procedures focus on:", c: ["Detecting material misstatements in assertions", "Control effectiveness", "Inherent risk assessment", "Management integrity"], a: 0, r: "Substantive procedures detect misstatements at assertion level."},
          {q: "Procedure providing evidence about completeness:", c: ["Tracing from source to accounting records", "Vouching from ledger to source", "Inspecting fixed assets", "Confirming receivables"], a: 0, r: "Tracing tests completeness; vouching tests occurrence."},
          {q: "Analytical procedures are required:", c: ["Planning and overall review stages", "Only during planning", "Only for substantive testing", "Only with effective controls"], a: 0, r: "Analytics mandatory in planning and final review."},
          {q: "Confirmation best tests which assertion?", c: ["Existence and rights for receivables", "Completeness of payables", "Valuation of inventory", "Presentation of equity"], a: 0, r: "Confirmations directly test existence and rights."},
          {q: "Vouching sales to shipping documents tests:", c: ["Occurrence assertion", "Completeness assertion", "Rights assertion", "Valuation assertion"], a: 0, r: "Vouching tests occurrence (transactions happened)."},
          {q: "Low assessed control risk implies:", c: ["Reduced substantive testing may be appropriate", "Controls can be ignored", "No substantive testing needed", "Higher detection risk required"], a: 0, r: "Effective controls allow reduced substantive scope."},
          {q: "Scanning involves:", c: ["Reviewing records for unusual items", "Detailed testing all transactions", "Sending confirmations", "Observing counts"], a: 0, r: "Scanning reviews for unusual items needing investigation."},
          {q: "Negative confirmation appropriate when:", c: ["Low risk, small balances, strong controls", "High fraud risk", "Material balances", "Weak controls"], a: 0, r: "Negative confirmations suit low-risk situations."},
          {q: "Inspection of tangible assets provides evidence about:", c: ["Existence assertion", "Completeness assertion", "Valuation assertion", "Rights and obligations"], a: 0, r: "Physical inspection confirms existence."},
          {q: "Reperformance involves:", c: ["Auditor independently executing procedures", "Observing client perform", "Reviewing calculations", "Testing controls design"], a: 0, r: "Reperformance means auditor independently performs procedure."},
          {q: "External confirmations least effective for:", c: ["Testing account completeness", "Verifying balances", "Testing existence", "Confirming agreements"], a: 0, r: "Confirmations don't effectively test completeness."},
          {q: "Inquiry alone provides:", c: ["Limited evidence requiring corroboration", "Sufficient appropriate evidence", "Highly reliable evidence", "No useful evidence"], a: 0, r: "Inquiry insufficient alone; requires corroboration."},
          {q: "Dual-purpose tests:", c: ["Test control effectiveness and substantive assertions", "Test two different controls", "Test two account balances", "Use two different procedures"], a: 0, r: "Dual-purpose tests evaluate controls and substantive details."},
          {q: "More persuasive evidence:", c: ["Evidence obtained directly by auditor", "Evidence from client", "Oral evidence", "Electronic images"], a: 0, r: "Direct auditor-obtained evidence is more reliable."},
          {q: "Cutoff testing addresses:", c: ["Transactions recorded in proper period", "All transactions recorded", "Balances valued correctly", "Controls operating"], a: 0, r: "Cutoff ensures proper period recording."},
          {q: "Observation provides evidence about:", c: ["Process performed at point in time", "Consistency over period", "Quantitative data accuracy", "Account balances"], a: 0, r: "Observation captures specific moment performance."},
          {q: "Tests of controls unnecessary when:", c: ["Not planning to rely on controls", "For all interim work", "For small entities only", "Never - always required"], a: 0, r: "If not relying on controls, testing unnecessary."},
          {q: "Increases evidence reliability:", c: ["Independent external sources", "Related parties", "Verbal representations", "Electronic copies"], a: 0, r: "Independence of source enhances reliability."},
          {q: "Account reconciliation tests:", c: ["Accuracy and existence of balances", "Control effectiveness", "Management integrity", "Fraud likelihood"], a: 0, r: "Reconciliations verify balance accuracy and existence."},
          {q: "Footing involves:", c: ["Adding numerical columns to verify totals", "Following items source to ledger", "Comparing between periods", "Inspecting documents"], a: 0, r: "Footing verifies mathematical accuracy of totals."},
          {q: "Management representations:", c: ["Supplement but don't replace procedures", "Provide sufficient evidence alone", "Unnecessary if controls strong", "Eliminate need for testing"], a: 0, r: "Representations corroborate but aren't sufficient alone."},
          {q: "Substantive analytical procedures appropriate when:", c: ["Relationships predictable and data reliable", "Controls weak", "Account immaterial", "Fraud suspected"], a: 0, r: "Analytics work when relationships stable and plausible."},
          {q: "Positive confirmation requests require:", c: ["Response whether agree or disagree", "Response only if disagree", "No response needed", "Auditor follow-up only"], a: 0, r: "Positive confirmations request response in all cases."},
          {q: "Most persuasive evidence combination:", c: ["Multiple types from independent sources", "Single highly reliable source", "Extensive inquiry", "Client representations"], a: 0, r: "Multiple types from independent sources most persuasive."},
          {q: "Recalculation tests:", c: ["Mathematical accuracy of records", "Control operating effectiveness", "Completeness of recording", "Transaction occurrence"], a: 0, r: "Recalculation verifies arithmetic accuracy."},
          {q: "Alternative procedures when confirmations not returned:", c: ["Inspect subsequent cash receipts and docs", "Send second request only", "Assume balance correct", "Adjust for non-responses"], a: 0, r: "Alternative procedures like cash receipts provide evidence."},
          {q: "Reliability affected by:", c: ["Source, nature, circumstances of creation", "Volume only", "Auditor's experience", "Client preference"], a: 0, r: "Multiple factors affect reliability."},
          {q: "Walk-through procedure involves:", c: ["Following transaction start to finish", "Touring facilities", "Observing inventory", "Interviewing all staff"], a: 0, r: "Walk-through traces transaction through entire process."},
          {q: "Directional testing means:", c: ["Designing tests based on assertion risk direction", "Testing chronologically", "Testing top-down only", "Following hierarchy"], a: 0, r: "Tests designed based on overstatement vs understatement risk."},
          {q: "Reduces extensive substantive procedures:", c: ["Strong controls and low control risk", "High inherent risk", "Complex transactions", "First-year audit"], a: 0, r: "Effective controls allow reduced substantive scope."},
          {q: "Subsequent events testing reviews:", c: ["Events between balance sheet and report date", "Only after report issuance", "Only during audit year", "Future projections"], a: 0, r: "Subsequent events are balance sheet to report date."},
          {q: "Inspection of documentation addresses:", c: ["Existence, occurrence, authorization", "Completeness primarily", "Valuation primarily", "Future viability"], a: 0, r: "Document inspection evidences existence and occurrence."},
          {q: "Negative assurance provided in:", c: ["Review engagements", "Audit engagements", "Compilation engagements", "Agreed-upon procedures"], a: 0, r: "Reviews provide negative assurance."},
          {q: "Stratification in sampling:", c: ["Divides population into subgroups", "Tests only high-value items", "Eliminates sampling risk", "Replaces random selection"], a: 0, r: "Stratification improves efficiency by grouping."},
          {q: "Non-statistical sampling:", c: ["Uses auditor judgment in selection", "Prohibits judgment", "Provides quantified risk", "Requires larger samples"], a: 0, r: "Non-statistical uses judgment; statistical uses math."},
          {q: "Tolerable misstatement in sampling:", c: ["Maximum acceptable before adjustment", "Actual misstatement found", "Overall materiality", "Trivial amount"], a: 0, r: "Tolerable misstatement is acceptable error level."},
          {q: "Controls testing sampling risk includes:", c: ["Over-reliance and under-reliance", "Only overstatement", "Only understatement", "No sampling risk"], a: 0, r: "Control testing has risks of assessing CR too low/high."},
          {q: "Discovery sampling used when:", c: ["Critical attribute rate expected near zero", "Many deviations expected", "Testing effectiveness", "Estimating balance"], a: 0, r: "Discovery finds at least one critical deviation."},
          {q: "Block sampling:", c: ["Selects consecutive items (not recommended)", "Random blocks", "Stratified groups", "Representative sample"], a: 0, r: "Block sampling may not be representative."},
          {q: "Projecting sample results:", c: ["Consider known and projected misstatement", "Use only actual found", "Ignore sampling risk", "Project only if material"], a: 0, r: "Total includes known + projected misstatement."},
          {q: "Increasing sample size:", c: ["Decreases sampling risk", "Eliminates sampling risk", "Increases efficiency", "No effect"], a: 0, r: "Larger samples reduce but don't eliminate sampling risk."},
          {q: "Sampling unit definition should:", c: ["Match audit objective and assertion", "Always be transactions", "Be monetary units", "Be customer accounts"], a: 0, r: "Unit definition depends on assertion tested."},
          {q: "Systematic sampling involves:", c: ["Selecting every nth item after random start", "Judgmental selection", "Haphazard selection", "Testing all items"], a: 0, r: "Systematic uses interval with random start."},
          {q: "Dual-purpose sample must:", c: ["Be large enough for both objectives", "Test controls only", "Test substantive only", "Use different items"], a: 0, r: "Size must satisfy both control and substantive objectives."},
          {q: "Tolerable rate of deviation:", c: ["Maximum control deviation acceptable", "Actual rate found", "Zero tolerance", "100% for details"], a: 0, r: "Tolerable rate is max acceptable before ineffective."},
          {q: "Expected misstatement affects:", c: ["Required sample size (larger if more expected)", "Selection method", "Tolerable misstatement", "Materiality"], a: 0, r: "Higher expected requires larger sample."},
          {q: "Qualitative factors in evaluation:", c: ["Nature, cause, implications of misstatements", "Only dollar amounts", "Only statistical precision", "Only sample size"], a: 0, r: "Qualitative assessment examines type, cause, implications."}
        ]
      },
      
      risk: {
        name: "Risk Assessment & Internal Control",
        questions: [
          {q: "Audit risk model: If IR and CR increase (AR fixed), auditor should:", c: ["Reduce acceptable detection risk (more substantive work)", "Increase detection risk", "Rely only on inquiry/analytics", "Issue disclaimer"], a: 0, r: "If IR/CR ↑ then DR must ↓ → more effective procedures."},
          {q: "Inherent risk is:", c: ["Susceptibility to misstatement before controls", "Risk controls fail", "Risk auditor fails", "Combined risk after procedures"], a: 0, r: "IR is risk of misstatement before considering controls."},
          {q: "Control risk represents:", c: ["Risk controls fail to prevent/detect misstatement", "Account susceptibility", "Auditor detection failure", "Overall audit risk"], a: 0, r: "CR is probability controls won't prevent/detect misstatement."},
          {q: "Detection risk is:", c: ["Risk auditor fails to detect material misstatement", "Risk of inherent errors", "Risk of control failures", "Total engagement risk"], a: 0, r: "DR is risk auditor's procedures won't detect misstatement."},
          {q: "High inherent risk requires:", c: ["More extensive substantive procedures", "Reduced substantive testing", "Eliminating control tests", "No additional procedures"], a: 0, r: "Higher IR means more risk requiring additional work."},
          {q: "Understanding internal control helps:", c: ["Identify risks and design procedures", "Eliminate substantive testing", "Guarantee no fraud", "Replace judgment"], a: 0, r: "IC understanding enables risk assessment and procedure design."},
          {q: "Five COSO IC components:", c: ["Control environment, risk assessment, control activities, info/communication, monitoring", "Only activities and monitoring", "Tests and substantive tests", "Planning, fieldwork, reporting"], a: 0, r: "COSO IC has five integrated components."},
          {q: "Control environment includes:", c: ["Tone at top, ethics, governance structure", "Specific procedures only", "Detective controls", "Audit procedures"], a: 0, r: "Control environment sets organizational tone and discipline."},
          {q: "Preventive controls:", c: ["Stop errors before they occur", "Find errors after occurrence", "Both prevent and detect", "Monitor other controls"], a: 0, r: "Preventive controls deter/prevent errors."},
          {q: "Detective controls:", c: ["Identify errors after they occur", "Prevent errors", "Eliminate all errors", "Replace preventive"], a: 0, r: "Detective controls find errors/irregularities after the fact."},
          {q: "Segregation of duties requires:", c: ["Different people for authorization, recording, custody", "Same person handles all", "Only two people", "Computer automation"], a: 0, r: "Segregation separates authorization, recordkeeping, custody."},
          {q: "Completeness assertion risk highest for:", c: ["Liabilities (unrecorded obligations)", "Assets (overstatement)", "Revenue (fraud)", "Equity (misstatement)"], a: 0, r: "Liabilities risk is understatement/incompleteness."},
          {q: "Occurrence assertion for revenue addresses:", c: ["Recorded sales actually happened", "All sales recorded", "Sales valued correctly", "Sales properly classified"], a: 0, r: "Occurrence tests whether recorded transactions are real."},
          {q: "Significant deficiency in IC:", c: ["Less severe than material weakness but warrants attention", "Same as material weakness", "Requires modified opinion", "Can be ignored"], a: 0, r: "Significant deficiency merits governance attention."},
          {q: "Material weakness means:", c: ["Reasonable possibility of material misstatement not prevented/detected", "Minor control problem", "Any deficiency", "Fraud exists"], a: 0, r: "Material weakness creates reasonable possibility material misstatement."},
          {q: "Compensating control:", c: ["Management review when segregation absent", "Additional authorization", "Backup files", "Audit procedures"], a: 0, r: "Compensating controls offset other weaknesses."},
          {q: "IT general controls include:", c: ["Access security, change management, backup/recovery", "Application validations", "Transaction processing logic", "Output reports"], a: 0, r: "IT general controls support applications and environment."},
          {q: "Application controls address:", c: ["Completeness, accuracy, validity of specific processing", "Broad IT environment", "Physical security", "Personnel policies"], a: 0, r: "Application controls ensure proper transaction processing."},
          {q: "Control activities include:", c: ["Authorization, reconciliations, physical controls", "Only management oversight", "Only segregation", "Audit procedures"], a: 0, r: "Control activities execute management directives."},
          {q: "Risk assessment process involves:", c: ["Identifying and analyzing risks to objectives", "Only financial statement risks", "External audit only", "Testing effectiveness"], a: 0, r: "Entity risk assessment identifies and analyzes risks."},
          {q: "Information system relevant to financial reporting must:", c: ["Support identification, capture, communication of info", "Only process journals", "Only generate reports", "Eliminate all errors"], a: 0, r: "IS must support identifying, capturing, processing, communicating."},
          {q: "Monitoring of controls includes:", c: ["Ongoing and separate evaluations", "Only year-end reviews", "Only external audits", "Internal audit only"], a: 0, r: "Monitoring involves continuous and periodic assessments."},
          {q: "Walk-through helps auditor:", c: ["Understand process flow and identify controls", "Test control effectiveness", "Perform substantive testing", "Issue audit report"], a: 0, r: "Walk-through traces transaction to understand process."},
          {q: "Service organization controls help when:", c: ["Client uses third party for significant functions", "All outsourcing", "No impact on audit", "Only IT functions"], a: 0, r: "SOC reports provide information about service org controls."},
          {q: "Understanding entity and environment includes:", c: ["Industry, regulation, business model, objectives", "Only financial results", "Only management", "Only internal controls"], a: 0, r: "Understanding encompasses industry, regulation, operations."},
          {q: "Fraud risk factors:", c: ["Incentive/pressure, opportunity, rationalization", "Only management fraud", "Only financial motivation", "Control weaknesses only"], a: 0, r: "Fraud triangle: incentive/pressure, opportunity, rationalization."},
          {q: "Revenue recognition fraud risk requires:", c: ["Presumption of fraud risk in revenue", "No special procedures", "Presumption never rebuttable", "Only SEC companies"], a: 0, r: "Standards presume fraud risk in revenue (rebuttable)."},
          {q: "Management override risk means:", c: ["Management can bypass controls", "Controls ineffective", "Audit procedures fail", "Fraud definitely exists"], a: 0, r: "Management has ability to override controls."},
          {q: "Auditor response to fraud risk:", c: ["Professional skepticism, unpredictable procedures, tested journal entries", "Accepting management", "Reducing procedures", "Issuing disclaimer"], a: 0, r: "Fraud risk requires heightened skepticism and specific tests."},
          {q: "Related party transactions require:", c: ["Understanding relationships and proper disclosure", "Automatic adjustment", "Modified opinion", "Scope limitation"], a: 0, r: "Related parties need identification and disclosure evaluation."},
          {q: "Going concern assessment considers:", c: ["Events within one year after financial statements", "Five-year projection", "Indefinite future", "Only past performance"], a: 0, r: "Going concern evaluation covers one year beyond FS date."},
          {q: "Substantive procedures alone (no control reliance):", c: ["More extensive testing of balances", "No documentation of controls", "Automatic disclaimer", "Management letter"], a: 0, r: "Substantive approach means more extensive detail testing."},
          {q: "Risk of material misstatement combines:", c: ["Inherent risk and control risk", "All three risk types", "Detection and audit risk", "Only control risk"], a: 0, r: "RMM is combination of inherent and control risk."},
          {q: "Analytical procedures in planning help:", c: ["Identify unusual relationships and risk areas", "Provide substantive evidence", "Test controls", "Replace other procedures"], a: 0, r: "Planning analytics identify areas needing attention."},
          {q: "Materiality affects:", c: ["Nature, timing, extent of procedures", "Only sample size", "Only reporting", "Only planning"], a: 0, r: "Materiality influences all aspects of audit."},
          {q: "Performance materiality is:", c: ["Amount less than overall for classes/accounts", "Same as overall", "Trivial threshold", "Reporting threshold"], a: 0, r: "Performance materiality set lower to reduce aggregation risk."},
          {q: "Tests of controls must be performed when:", c: ["Auditor plans reliance or substantive alone insufficient", "Always required", "Never for small entities", "Only SEC clients"], a: 0, r: "Control tests required if relying or substantive inadequate."},
          {q: "Dual-dated report used when:", c: ["Subsequent event requires disclosure after original date", "Two auditors involved", "Two opinions issued", "Two years audited"], a: 0, r: "Dual dating extends responsibility for specific event only."},
          {q: "Limitations of internal control:", c: ["Management override, human error, collusion", "Cost of controls", "Only human error", "Only technological failures"], a: 0, r: "IC inherently limited by override, errors, collusion."},
          {q: "Auditor must communicate to governance:", c: ["Significant deficiencies and material weaknesses", "All control deficiencies", "Only material weaknesses", "No control matters"], a: 0, r: "Significant deficiencies and weaknesses require communication."},
          {q: "Understanding predecessor's work:", c: ["Review workpapers and communications", "No review needed", "Only management inquiries", "Only financial statements"], a: 0, r: "Successor should review predecessor's workpapers."},
          {q: "Opening balances for initial audit:", c: ["Sufficient evidence prior balances correct", "Reliance on predecessor only", "No additional work", "Always qualified"], a: 0, r: "Initial audits require verifying opening balances."},
          {q: "Small entity considerations:", c: ["Control environment assessment remains critical", "Controls can be ignored", "No IC understanding needed", "Only substantive testing"], a: 0, r: "Even small entities require understanding controls."},
          {q: "IT control environment assessment:", c: ["Governance, security, change management", "Only access controls", "Only backups", "Only application logic"], a: 0, r: "IT control environment includes governance, security, operations."},
          {q: "User access controls address:", c: ["Who can access systems and data", "Data backup only", "Change management", "Application processing"], a: 0, r: "Access controls restrict system/data access to authorized users."},
          {q: "Change management controls ensure:", c: ["Proper authorization and testing of changes", "No changes occur", "Changes happen quickly", "Developers have production access"], a: 0, r: "Change management controls proper authorization and testing."},
          {q: "Automated controls benefit:", c: ["Consistent application when designed properly", "Eliminate all errors", "No monitoring needed", "Replace all manual"], a: 0, r: "Automated controls apply consistently when properly designed."},
          {q: "Data analytics in audit:", c: ["Can enhance risk assessment and testing", "Replaces judgment", "Eliminates sampling", "Only for large audits"], a: 0, r: "Analytics enhance audit but don't replace judgment."},
          {q: "Professional skepticism toward controls:", c: ["Critically assessing design and implementation", "Assuming controls don't work", "Accepting management assertions", "Testing optional"], a: 0, r: "Skepticism requires critical evaluation throughout."},
          {q: "Substantive procedures can never:", c: ["Be completely eliminated even with strong controls", "Be performed before year-end", "Include analytical procedures", "Test account balances"], a: 0, r: "Some substantive procedures always required regardless of controls."}
        ]
      },
      
      reporting: {
        name: "Forming Conclusions & Reporting",
        questions: [
          {q: "Unmodified opinion states:", c: ["FS fairly presented in all material respects", "FS are absolutely accurate", "No misstatements exist", "All accounts correct"], a: 0, r: "Unmodified opinion concludes fair presentation, not perfection."},
          {q: "Qualified opinion uses phrase:", c: ["'Except for' the effects of matter described", "FS not fairly presented", "Unable to obtain evidence", "Not independent"], a: 0, r: "Qualified opinions use 'except for' language."},
          {q: "Adverse opinion means:", c: ["FS not fairly presented due to pervasive GAAP departure", "Scope limitation", "Lack of independence", "Substantial doubt going concern"], a: 0, r: "Adverse opinion states FS materially and pervasively misstated."},
          {q: "Disclaimer of opinion results from:", c: ["Pervasive scope limitation or lack independence", "Material GAAP departure", "Going concern issue", "Related party transactions"], a: 0, r: "Disclaimer when unable to obtain evidence or not independent."},
          {q: "Material but not pervasive GAAP departure:", c: ["Qualified opinion", "Adverse opinion", "Disclaimer", "Unmodified opinion"], a: 0, r: "Material but not pervasive warrants qualified opinion."},
          {q: "Pervasive scope limitation leads to:", c: ["Disclaimer of opinion", "Qualified opinion", "Adverse opinion", "Unmodified with emphasis"], a: 0, r: "Pervasive scope limitation prevents opinion → disclaimer."},
          {q: "Emphasis-of-matter paragraph:", c: ["Draws attention to matter in FS without modifying opinion", "Modifies the opinion", "Replaces basis for opinion", "Used for scope limitations"], a: 0, r: "EOM highlights properly disclosed matters without modifying opinion."},
          {q: "Other-matter paragraph:", c: ["Refers to matter not in FS relevant to audit/report", "Discusses FS misstatements", "Modifies opinion", "Replaces emphasis"], a: 0, r: "OM addresses matters not in FS but relevant to understanding."},
          {q: "Going concern substantial doubt requires:", c: ["Disclosure evaluation and possible emphasis paragraph", "Automatic disclaimer", "Adverse opinion", "Qualified opinion"], a: 0, r: "Going concern requires evaluating disclosure and possibly emphasis."},
          {q: "Required audit report elements:", c: ["Title, addressee, opinion, basis, responsibilities, signature, date", "Only opinion paragraph", "Opinion and signature", "Opinion and date"], a: 0, r: "Standard report has specific required elements."},
          {q: "Auditor's opinion paragraph addresses:", c: ["Whether FS are fairly presented per framework", "Control effectiveness", "Fraud absence", "Management competence"], a: 0, r: "Opinion paragraph states conclusion on FS fair presentation."},
          {q: "Basis for opinion section includes:", c: ["Reference to GAAS, independence, reasonable assurance", "Detailed procedures performed", "All evidence obtained", "Materiality calculations"], a: 0, r: "Basis section confirms GAAS compliance and independence."},
          {q: "Management's responsibility for FS:", c: ["Preparation per framework and internal control", "Auditing the statements", "Guaranteeing accuracy", "Hiring auditor"], a: 0, r: "Management responsible for FS preparation and maintaining IC."},
          {q: "Auditor's responsibility:", c: ["Express opinion based on audit per GAAS", "Prepare financial statements", "Prevent all fraud", "Guarantee FS accuracy"], a: 0, r: "Auditor expresses opinion; doesn't prepare FS."},
          {q: "Report date should be:", c: ["No earlier than date auditor obtained sufficient evidence", "Balance sheet date", "Fieldwork start date", "Client's preference"], a: 0, r: "Report dated when auditor obtained sufficient evidence."},
          {q: "Comparative financial statements require:", c: ["Opinion on each period presented", "Opinion on current year only", "Combined opinion all years", "No prior year reference"], a: 0, r: "Auditor reports on each period presented."},
          {q: "Updated report on prior period:", c: ["Expresses current opinion on prior period", "Repeats original opinion only", "Is prohibited", "Requires reaudit"], a: 0, r: "Updated report expresses current opinion based on current knowledge."},
          {q: "Predecessor auditor's report may be:", c: ["Reissued or referenced by successor", "Ignored completely", "Updated by successor", "Invalidated"], a: 0, r: "Predecessor may reissue or successor may reference."},
          {q: "Unable to attend physical inventory may cause:", c: ["Qualified or disclaimer depending on materiality", "Automatic adverse", "Unmodified always", "No impact"], a: 0, r: "Inventory scope limitation may require modification."},
          {q: "Client refuses to disclose related parties:", c: ["GAAP departure → qualified or adverse", "Scope limitation", "Disclaimer", "Unmodified with emphasis"], a: 0, r: "Inadequate disclosure is GAAP departure."},
          {q: "Key audit matters (KAM):", c: ["Required for listed entities under ISA", "Required all audits", "Optional for US GAAS", "Same as emphasis matters"], a: 0, r: "KAM required for listed entities under ISA."},
          {q: "Critical audit matters (CAM):", c: ["Required for larger accelerated filers (SEC)", "Required all public companies", "Required private companies", "Prohibited by PCAOB"], a: 0, r: "CAM required by PCAOB for large accelerated filers."},
          {q: "CAM must:", c: ["Relate to material accounts and be challenging/subjective", "Include all difficult judgments", "Repeat all procedures", "Provide separate opinion"], a: 0, r: "CAM are material matters involving challenging judgment."},
          {q: "Subsequent events are:", c: ["Events between balance sheet and report date", "Events after report issuance", "Only adjusting events", "Future projections"], a: 0, r: "Subsequent events occur balance sheet to report date."},
          {q: "Type I subsequent events require:", c: ["Adjustment to financial statements", "Disclosure only", "No action", "Modified opinion"], a: 0, r: "Type I events provide evidence about conditions at BS date."},
          {q: "Type II subsequent events require:", c: ["Disclosure if material", "Adjustment to FS", "Modified opinion", "No action"], a: 0, r: "Type II arose after balance sheet date → disclosure if material."},
          {q: "Subsequent event after report but before FS issuance:", c: ["May require amended FS and dual-dated report", "No auditor responsibility", "Automatic disclaimer", "New audit required"], a: 0, r: "Material subsequent events may require amendment and dual dating."},
          {q: "Discovers facts after report issuance:", c: ["Assess impact and discuss with management/governance", "Immediately issue corrected report", "Ignore if immaterial", "Notify all users"], a: 0, r: "Subsequent discovery requires assessment and discussion."},
          {q: "Review engagement provides:", c: ["Limited/negative assurance", "Reasonable/positive assurance", "No assurance", "Absolute assurance"], a: 0, r: "Review provides limited assurance."},
          {q: "Review procedures primarily:", c: ["Inquiry and analytical procedures", "Tests of controls", "Substantive detail testing", "Physical observation"], a: 0, r: "Reviews rely mainly on inquiry and analytics."},
          {q: "Compilation engagement provides:", c: ["No assurance on financial statements", "Limited assurance", "Reasonable assurance", "Positive assurance"], a: 0, r: "Compilation provides no assurance."},
          {q: "Compilation report states:", c: ["No audit/review performed, no assurance expressed", "Limited assurance provided", "FS are accurate", "Controls tested"], a: 0, r: "Compilation report explicitly states no assurance."},
          {q: "Agreed-upon procedures:", c: ["Specific procedures, summary of findings, no opinion", "Provide opinion", "Substitute for audit", "Provide assurance"], a: 0, r: "AUP performs specified procedures and reports findings."},
          {q: "Preparation engagement:", c: ["Prepares FS, no assurance or report issued", "Issues review report", "Provides limited assurance", "Requires independence"], a: 0, r: "Preparation helps prepare FS with no assurance."},
          {q: "Attestation engagement:", c: ["Conclusion on subject matter per criteria", "Only financial statements", "No report issued", "Compilation services"], a: 0, r: "Attestation examines/reviews subject matter against criteria."},
          {q: "Examination attestation provides:", c: ["Reasonable assurance (opinion)", "Limited assurance", "No assurance", "Absolute certainty"], a: 0, r: "Examination provides reasonable assurance similar to audit."},
          {q: "Review attestation provides:", c: ["Limited assurance (conclusion)", "Reasonable assurance", "No assurance", "Opinion"], a: 0, r: "Review attestation provides limited assurance conclusion."},
          {q: "Management representations:", c: ["Required written from management", "Optional if controls strong", "Replace other evidence", "Sufficient alone"], a: 0, r: "Written representations required but supplement evidence."},
          {q: "Attorney letter requests information:", c: ["Litigation, claims, assessments", "All legal matters", "Tax positions", "Contract disputes only"], a: 0, r: "Attorney letters address litigation, claims, assessments."},
          {q: "Other information in annual report:", c: ["Read for material inconsistency with FS", "Not auditor's responsibility", "Must be audited", "Automatically correct"], a: 0, r: "Auditor reads other info for material inconsistencies."},
          {q: "Material inconsistency in other information:", c: ["Requesting revision or other matter paragraph", "Modified opinion on FS", "Disclaimer", "No action"], a: 0, r: "Material inconsistency may require other-matter paragraph."},
          {q: "Group audit (component auditors):", c: ["Group auditor assuming responsibility or referencing", "Always referencing components", "Never using components", "Separate opinions"], a: 0, r: "Group auditor assumes responsibility or references components."},
          {q: "Referencing component auditor:", c: ["Divides responsibility, names component in report", "Group retains full responsibility", "Not permitted", "Only foreign components"], a: 0, r: "Referencing divides responsibility and identifies component."},
          {q: "Service organization report (SOC 1):", c: ["Controls relevant to user financial reporting", "All service org controls", "Privacy controls", "Compliance controls"], a: 0, r: "SOC 1 reports on controls relevant to user FS."},
          {q: "Audit documentation must:", c: ["Support conclusions and comply with GAAS", "Include all information reviewed", "Be provided to client", "Be retained indefinitely"], a: 0, r: "Documentation supports conclusions and demonstrates GAAS compliance."},
          {q: "Documentation retention period:", c: ["Minimum 5 years SEC, 7 for PCAOB", "1 year", "Indefinite", "3 years all"], a: 0, r: "SEC rules require 7 years; PCAOB also 7."},
          {q: "Engagement quality review required for:", c: ["SEC issuer audits and certain high-risk", "All audits", "Only Big 4 firms", "Only financial statement audits"], a: 0, r: "Quality review required for issuers and high-risk."},
          {q: "Engagement letter establishes:", c: ["Terms, responsibilities, scope of engagement", "Fee amount only", "Audit procedures", "FS preparation"], a: 0, r: "Engagement letter documents understanding of terms."},
          {q: "Quality control at firm level addresses:", c: ["Leadership, ethics, acceptance, performance, monitoring", "Only individual engagement", "Only partner competence", "Only independence"], a: 0, r: "Firm quality control encompasses multiple elements."},
          {q: "When issuing qualified opinion:", c: ["'Except for' paragraph added describing issue", "Opinion section only modified", "No changes to report structure", "Basis section removed"], a: 0, r: "Qualified opinion adds except for paragraph and modifies opinion."}
        ]
      }
    };

    // App logic
    const LS_KEY = 'aud_study_stats_v1';
    let stats = loadStats();
    let currentTopic = null;
    let quiz = null;
    let quizSize = 25;

    function loadStats() {
      try {
        const data = localStorage.getItem(LS_KEY);
        if (!data) return initStats();
        const parsed = JSON.parse(data);
        Object.keys(parsed).forEach(key => {
          if (Array.isArray(parsed[key].seen)) {
            parsed[key].seen = new Set(parsed[key].seen);
          }
        });
        return parsed;
      } catch {
        return initStats();
      }
    }

    function initStats() {
      const s = {};
      Object.keys(TOPICS).forEach(key => {
        s[key] = { seen: new Set(), correct: 0, wrong: 0 };
      });
      return s;
    }

    function saveStats() {
      try {
        const toSave = {};
        Object.keys(stats).forEach(key => {
          toSave[key] = {
            seen: Array.from(stats[key].seen),
            correct: stats[key].correct,
            wrong: stats[key].wrong
          };
        });
        localStorage.setItem(LS_KEY, JSON.stringify(toSave));
      } catch (e) {
        console.error('Save failed:', e);
      }
    }

    // DOM
    const homeScreen = document.getElementById('homeScreen');
    const quizScreen = document.getElementById('quizScreen');
    const topicGrid = document.getElementById('topicGrid');
    const sizeSlider = document.getElementById('sizeSlider');
    const sizeLabel = document.getElementById('sizeLabel');
    const startBtn = document.getElementById('startBtn');
    const resetBtn = document.getElementById('resetBtn');
    const topicLabel = document.getElementById('topicLabel');
    const progressLabel = document.getElementById('progressLabel');
    const progressBar = document.getElementById('progressBar');
    const correctStat = document.getElementById('correctStat');
    const wrongStat = document.getElementById('wrongStat');
    const scoreStat = document.getElementById('scoreStat');
    const questionText = document.getElementById('questionText');
    const choicesDiv = document.getElementById('choicesDiv');
    const rationaleDiv = document.getElementById('rationaleDiv');
    const showBtn = document.getElementById('showBtn');
    const nextBtn = document.getElementById('nextBtn');
    const exitBtn = document.getElementById('exitBtn');

    function renderTopics() {
      topicGrid.innerHTML = '';
      Object.entries(TOPICS).forEach(([key, topic]) => {
        const s = stats[key];
        const seen = s.seen.size;
        const total = topic.questions.length;
        const pct = Math.round((seen / total) * 100);
        
        const btn = document.createElement('button');
        btn.className = 'topic-btn';
        if (currentTopic === key) btn.classList.add('selected');
        btn.innerHTML = `
          <div>
            <div style="font-size: 17px; margin-bottom: 6px;">${topic.name}</div>
            <div style="font-size: 13px; opacity: 0.7;">${seen}/${total} seen • ${pct}% complete</div>
          </div>
          <div class="badge">${total}Q</div>
        `;
        btn.addEventListener('click', () => {
          currentTopic = key;
          renderTopics();
          startBtn.textContent = `Start ${topic.name}`;
          startBtn.disabled = false;
        });
        topicGrid.appendChild(btn);
      });
    }

    sizeSlider.addEventListener('input', () => {
      quizSize = parseInt(sizeSlider.value);
      sizeLabel.textContent = quizSize;
    });

    startBtn.addEventListener('click', () => {
      if (!currentTopic) return;
      const topic = TOPICS[currentTopic];
      const questions = [...topic.questions].sort(() => Math.random() - 0.5).slice(0, quizSize);
      
      quiz = {
        topicKey: currentTopic,
        questions,
        currentIndex: 0,
        correct: 0,
        wrong: 0,
        answered: false
      };
      
      homeScreen.style.display = 'none';
      quizScreen.style.display = 'block';
      renderQuestion();
    });

    function renderQuestion() {
      const q = quiz.questions[quiz.currentIndex];
      quiz.answered = false;
      
      topicLabel.textContent = TOPICS[quiz.topicKey].name;
      progressLabel.textContent = `${quiz.currentIndex + 1}/${quiz.questions.length}`;
      progressBar.style.width = `${((quiz.currentIndex + 1) / quiz.questions.length) * 100}%`;
      
      correctStat.textContent = quiz.correct;
      wrongStat.textContent = quiz.wrong;
      const total = quiz.correct + quiz.wrong;
      scoreStat.textContent = total > 0 ? `${Math.round((quiz.correct / total) * 100)}%` : '0%';
      
      questionText.textContent = q.q;
      
      choicesDiv.innerHTML = '';
      q.c.forEach((choice, idx) => {
        const div = document.createElement('div');
        div.className = 'choice';
        div.textContent = `${String.fromCharCode(65 + idx)}. ${choice}`;
        div.addEventListener('click', () => selectAnswer(idx));
        choicesDiv.appendChild(div);
      });
      
      rationaleDiv.style.display = 'none';
      showBtn.disabled = false;
      nextBtn.textContent = quiz.currentIndex < quiz.questions.length - 1 ? 'Next →' : 'Finish';
    }

    function selectAnswer(idx) {
      if (quiz.answered) return;
      
      const q = quiz.questions[quiz.currentIndex];
      const isCorrect = idx === q.a;
      quiz.answered = true;
      
      const qIndex = TOPICS[quiz.topicKey].questions.indexOf(q);
      stats[quiz.topicKey].seen.add(qIndex);
      
      if (isCorrect) {
        quiz.correct++;
        stats[quiz.topicKey].correct++;
      } else {
        quiz.wrong++;
        stats[quiz.topicKey].wrong++;
      }
      saveStats();
      
      const choices = choicesDiv.children;
      for (let i = 0; i < choices.length; i++) {
        choices[i].classList.add('disabled');
        if (i === q.a) choices[i].classList.add('correct');
        if (i === idx && !isCorrect) choices[i].classList.add('wrong');
      }
      
      rationaleDiv.textContent = (isCorrect ? '✅ Correct! ' : '❌ Incorrect. ') + q.r;
      rationaleDiv.style.display = 'block';
      showBtn.disabled = true;
      
      correctStat.textContent = quiz.correct;
      wrongStat.textContent = quiz.wrong;
      const total = quiz.correct + quiz.wrong;
      scoreStat.textContent = `${Math.round((quiz.correct / total) * 100)}%`;
    }

    showBtn.addEventListener('click', () => {
      if (!quiz.answered) {
        const q = quiz.questions[quiz.currentIndex];
        rationaleDiv.textContent = '💡 ' + q.r;
        rationaleDiv.style.display = 'block';
      }
    });

    nextBtn.addEventListener('click', () => {
      if (quiz.currentIndex < quiz.questions.length - 1) {
        quiz.currentIndex++;
        renderQuestion();
      } else {
        const score = Math.round((quiz.correct / (quiz.correct + quiz.wrong)) * 100);
        alert(`🎉 Quiz Complete!\n\n Score: ${quiz.correct}/${quiz.correct + quiz.wrong} (${score}%)\n\nGreat work! Keep practicing.`);
        exitQuiz();
      }
    });

    exitBtn.addEventListener('click', exitQuiz);

    function exitQuiz() {
      quizScreen.style.display = 'none';
      homeScreen.style.display = 'block';
      currentTopic = null;
      startBtn.textContent = 'Select a topic to begin';
      startBtn.disabled = true;
      renderTopics();
    }

    resetBtn.addEventListener('click', () => {
      if (!confirm('Reset all progress for all topics? This cannot be undone.')) return;
      stats = initStats();
      saveStats();
      renderTopics();
      alert('All progress has been reset.');
    });

    // Initialize
    renderTopics();
  </script>
</body>
</html>
