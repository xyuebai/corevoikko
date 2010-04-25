/* Libvoikko: Library of Finnish language tools
 * Copyright (C) 2010 Harri Pitkänen <hatapitk@iki.fi>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *********************************************************************************/

#ifndef VOIKKO_GRAMMAR_CHECK_SENTENCE_CHECK
#define VOIKKO_GRAMMAR_CHECK_SENTENCE_CHECK

#include "grammar/Sentence.hpp"
#include "setup/setup.hpp"

namespace libvoikko { namespace grammar { namespace check {
/**
 * Interface for sentence based grammar checkers.
 */
class SentenceCheck {
	public:
		/**
		 * Checks given sentence and adds errors to grammar checker cache.
		 */
		virtual void check(voikko_options_t * options, const Sentence * sentence) = 0;
		
		virtual ~SentenceCheck();
};

} } }

#endif