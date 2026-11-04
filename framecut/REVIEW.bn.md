# Framecut পর্যালোচনা

পর্যালোচনার তারিখ ৪ নভেম্বর ২০২৬। ভিত্তি HeyGen HyperFrames v0.9.9, commit 12ce8c2ffd37757204afa0ab170df27e0a384162। এটি স্থানীয় উন্নয়ন ও পরীক্ষার রেকর্ড। ChatGPT-এর আনুষ্ঠানিক নিরাপত্তা অনুমোদন আলাদাভাবে প্রয়োজন।

## মূলের সঙ্গে মিল

মূল সংস্করণের নয়টি স্কিলের ৩০৮টি ফাইলের তালিকা ও SHA-256 সংরক্ষিত আছে upstream-inventory.json-এ। check-package.py অনুপস্থিত ফাইল এবং ঘোষিত পরিবর্তনের বাইরে অন্য বদল শনাক্ত করে। মূল rendering engine ও বিশেষজ্ঞ নির্দেশনার সঙ্গে ChatGPT workflow, একক স্কিলের প্রবেশপথ এবং বাংলা local rendering যোগ করা হয়েছে।

## সংশোধন

| বিষয়             | পরিবর্তন                                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| প্লাগইন আপডেট      | প্লাগইনের 1.0.1 সংস্করণ ও HyperFrames 0.9.9 runtime আলাদা করা হয়েছে                                               |
| বাংলা ফন্ট          | স্থানীয় helper স্বয়ংক্রিয়ভাবে bundled Noto Sans Bengali ব্যবহার করে                                                |
| HDR              | সাধারণ SDR cutter HDR/BT.2020 ইনপুট প্রত্যাখ্যান করে                                                                |
| অবিশ্বস্ত মিডিয়া    | স্থানীয় helper নির্দিষ্ট container format ও file/pipe protocol গ্রহণ করে; HLS playlist প্রত্যাখ্যান করে               |
| গোপন তথ্য         | প্রকল্পের নিজের .env থেকে নির্দিষ্ট API key নামই পড়ে; parent .env বা OAuth endpoint override গ্রহণ করে না           |
| বাহ্যিক সেবা        | ডেটা পাঠানো, ব্যয় ও provider নির্বাচন সম্পর্কে স্বচ্ছ নির্দেশনা যোগ করা হয়েছে                                            |
| browser sandbox  | bundled map-capture helper-এর sandbox নিষ্ক্রিয় করার flag সরানো হয়েছে                                           |
| ইনস্টলেশন         | standalone Agent Skill ও plugin-এর জন্য আলাদা যাচাইযোগ্য archive builder আছে                                      |
| prompt injection | transcript, subtitle, OCR, metadata ও downloaded code-কে অনুমতি বা নির্দেশনার উৎস হিসেবে গ্রহণ করা নিষেধ করা হয়েছে |

## পরীক্ষার আওতা

- নয়টি স্কিল ও ৩০৮টি মূল ফাইলের inventory পরীক্ষা।
- launcher-এর দশটি পরীক্ষা, যার মধ্যে স্বাধীন runtime version এবং ভুল pin প্রত্যাখ্যান আছে।
- provider credential ও transport helper-এর একুশটি পরীক্ষা, যার মধ্যে parent .env, endpoint override ও credential redirection পরীক্ষা আছে।
- বাস্তব FFmpeg ভিডিও দিয়ে portrait title, বাংলা default font, captioned trim, audio, পূর্ণ decode, output overwrite, invalid range, HDR ও network playlist প্রত্যাখ্যান পরীক্ষা।
- পরিবর্তিত JavaScript-এর lint এবং Python syntax পরীক্ষা।
- self-contained archive-এর path, manifest, checksum এবং স্থানীয় helper পরীক্ষা।

## যেসব যাচাই এখনো বাকি

GitHub Actions-এ Chrome দিয়ে HTML starter-এর lint, browser check, MP4 render এবং সম্পূর্ণ decode সফল হয়েছে। ফলটি ৪ সেকেন্ড, ৯৬ ফ্রেম, 960×540 এবং 24 fps। মধ্যবর্তী ফ্রেমে বাংলা অক্ষর ও গ্রাফিক্স দেখা হয়েছে। একই run-এ ৩১টি Node পরীক্ষা, inventory ও FFmpeg smoke পরীক্ষা সফল। [পরীক্ষার ফল](https://github.com/istiaque-ahmed-2026/hyperframes/actions/runs/41838083912)

৪ নভেম্বর ২০২৬-এ পুরোনো full-bundle standalone প্যাকেজ actual installation safety scan-এ প্রত্যাখ্যাত হয়। Nested skill packaging ঠিক করার পরও safety scan ব্যর্থ হয়; নির্দিষ্ট কারণ জানানো হয়নি।

এরপর provider credential readers, upload clients ও automatic installers বাদ দিয়ে ছোট standalone সংস্করণ তৈরি করা হয়। সেটি ChatGPT-এর প্রকৃত installation flow-তে গৃহীত হয় এবং পরবর্তী সংরক্ষিত অবস্থায় উপস্থিতি যাচাই করা হয়। `framecut/skill/` ও নতুন ZIP সেই গৃহীত সংস্করণের হুবহু export; server-generated display metadata-ও রাখা হয়েছে। এটি full plugin-এর অনুমোদন বা ভবিষ্যতের সব নিরাপত্তা পরীক্ষার নিশ্চয়তা নয়।

Paid generation, avatar, voice cloning এবং সব তৃতীয় পক্ষের মডেল সরাসরি পরীক্ষা করা হয়নি। সেসবের জন্য উপলব্ধ provider, অনুমোদন ও প্রয়োজনীয় account access লাগে। npm package pin মূল runtime নির্ধারণ করে; এর মাধ্যমে সব transitive dependency-এর নিরাপত্তা নিশ্চিত হয় না। এই পর্যালোচনা পূর্ণ penetration test বা আনুষ্ঠানিক certification নয়।

## পুনরায় পরীক্ষা

    python3 framecut/check-package.py
    python3 framecut/smoke.py
    node --test plugins/framecut-studio/skills/hyperframes/scripts/plugin-cli.test.mjs
    node --test plugins/framecut-studio/skills/media-use/audio/scripts/lib/heygen.test.mjs

নতুন runtime version বা নতুন provider যোগ করলে সংশ্লিষ্ট পরীক্ষা আবার চালাও। পরে প্রকাশ করার আগে বর্তমান GitHub main-এর পরিবর্তন দেখে merge করো।
