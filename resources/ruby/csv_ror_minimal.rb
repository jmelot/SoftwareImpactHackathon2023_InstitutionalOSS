#!/usr/bin/env ruby

require 'bundler/setup'
require 'http'
require 'active_support/all'
require 'csv'
require 'byebug'

class SoftwareRor
  attr_accessor :software_name, :github_slug, :ror_id, :org_name, :extraction_methods

  def initialize(software_name:, github_slug:, ror_id:, org_name:, extraction_methods:)
    @software_name = software_name
    @github_slug = github_slug
    @ror_id = ror_id
    @org_name = org_name
    @extraction_methods = extraction_methods
  end
end

# we want to import various sources of information
output_array = []

# ------
# import the csv working_file_with_rors_added_by_name.csv and extract relevant info
# ------

in_file = '../working_file_with_rors_added_by_name.csv'
csv = CSV.read(File.expand_path(File.join(__dir__, in_file)), headers: true)
csv.each do |row|
  if (row['ROR and other mappings'].blank? || row['ROR and other mappings'] == '#N/A' || row['ROR and other mappings'] == '0' ) &&
     row['proposed_ror_id'].blank?
    next
  end


  ror, extraction_methods = if row['ROR and other mappings'].blank? || row['ROR and other mappings'] == '#N/A'
                              [ row['proposed_ror_id'], 'by_name' ]
                            else
                              [ row['ROR and other mappings'], 'human_curated' ]
                            end

  sfw_name = row['Resource_Name']
  org_name = if row['Parent Org Name'].blank? || row['Parent Org Name'] == '#N/A'
               row['proposed_name']
             else
               row['Parent Org Name']
             end

  # github slug is sometimes in Resource_URL or Alternate_URLs

  github_slug = ''
  github_urls = ''
  github_urls = row['Resource_URL'] if row['Resource_URL']&.include?('github.com')
  github_urls = row['Alternate_URLs'] if github_urls.blank? && row['Alternate_URLs']&.include?('github.com')
  github_url = github_urls.split(',').select{|i| i.include?('github.com') }.first
  m = github_url.match(/^https:\/\/github.com\/(.+\/.+)$/) if github_url.present?
  github_slug = m[1] if m

  org_name = org_name.split(';').first if org_name.include?(';') # to make the org names more consistent

  output_array << SoftwareRor.new(software_name: sfw_name, github_slug: github_slug, ror_id: ror,
                                  org_name: org_name, extraction_methods: extraction_methods)
end

# ------
# output a CSV with only basic info
# ------

out_file = '../working_file_minimal.csv'
CSV.open(File.expand_path(File.join(__dir__, out_file)), 'w') do |csv_out|
  csv_out << %w[software_name github_slug ror_id org_name extraction_methods]
  output_array.each do |sr|
    csv_out << [sr.software_name, sr.github_slug, sr.ror_id, sr.org_name, sr.extraction_methods]
  end
end

puts "Output file #{out_file}"
