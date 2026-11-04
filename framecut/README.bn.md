# Framecut Video — ChatGPT স্কিল

[আপডেটেড ZIP ডাউনলোড](downloads/framecut-video-skill.zip?raw=true)। এই প্যাকেজটি আগের standalone ZIP-এর পরিবর্তে ব্যবহার করো।

ChatGPT-কে ZIP দিয়ে স্কিল হিসেবে যোগ করতে বলো। GitHub লিংক দিলে এই রেপোর `framecut/skill/` ফোল্ডারটি নির্দিষ্ট করো। পুরো রেপোর সব স্কিল ইনস্টল করতে বলবে না। শুধু লিংক পড়া মানে ইনস্টল হওয়া নয়।

৪ নভেম্বর ২০২৬-এ এই সংস্করণটি প্রকৃত ChatGPT ইনস্টলেশন প্রক্রিয়ায় গৃহীত হয়েছিল। এটি ভবিষ্যতের সব পরীক্ষার নিশ্চয়তা নয়। আগের full-bundle standalone প্যাকেজ নিরাপত্তা পরীক্ষায় প্রত্যাখ্যাত হয়েছিল।

বাংলা টাইটেল, caption ও trim-এর স্থানীয় helper এবং বাংলা ফন্ট আছে। Python 3, FFmpeg ও ffprobe লাগবে। উন্নত animation-এর জন্য অনুমোদিত HyperFrames renderer এবং AI generation-এর জন্য অনুমোদিত media tool লাগবে। সরাসরি credential পড়া, provider upload বা স্বয়ংক্রিয় dependency installation-এর কোড এই স্কিলে নেই।

উদাহরণ: “Framecut Video দিয়ে দৃশ্যপট নামে ৪ সেকেন্ডের বাংলা টাইটেল বানাও। MP4 দাও।”

পুরোনো `plugins/framecut-studio/` আলাদা plugin; সেটির জন্য এই personal skill-এর গ্রহণযোগ্যতার ফল প্রযোজ্য নয়।
